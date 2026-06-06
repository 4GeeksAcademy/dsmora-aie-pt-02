import asyncio
import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent.parent


async def scrape_tutorial(context, output_dir: Path, tutorial_name: str, url: str):
    output_file = output_dir / f"{tutorial_name}.json"
    label = f"{output_dir.name}/{tutorial_name}"

    print(f"\n=== Tutorial: {label} ===")
    print(f"[{label}] Abriendo {url}...")

    page = await context.new_page()
    try:
        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(10000)

        async def clear_modals():
            await page.evaluate('''() => {
                const modals = document.querySelectorAll('.self-closing-modal, [class*="modal"]');
                modals.forEach(m => m.remove());
            }''')

        await clear_modals()
        toggle = await page.query_selector("button#sidebar-toggle")
        if toggle:
            state = await toggle.get_attribute("data-state")
            if state == "closed":
                print(f"[{label}] Abriendo menu lateral...")
                await toggle.click(force=True)
                await page.wait_for_timeout(2000)

        cards = await page.query_selector_all("div.exercise-card")
        print(f"[{label}] Se encontraron {len(cards)} lecciones.")

        results = []

        for i in range(len(cards)):
            await clear_modals()
            current_cards = await page.query_selector_all("div.exercise-card")
            if i >= len(current_cards):
                break
            card = current_cards[i]

            title_text = await card.inner_text()
            title_text = " ".join(title_text.split())
            print(f"[{label}] Procesando leccion {i + 1}/{len(cards)}: {title_text}")

            await card.click(force=True)
            await page.wait_for_timeout(4000)

            # Intentar avanzar si aparecen bloqueos
            for _ in range(2):
                try:
                    anyway = await page.get_by_role("button", name="Continue anyway").element_handle()
                    if anyway and await anyway.is_visible():
                        print(f"[{label}] Click 'Continue anyway'")
                        await anyway.click(force=True)
                        await page.wait_for_timeout(2000)

                    cont = await page.query_selector("div.continue-button")
                    if cont and await cont.is_visible():
                        print(f"[{label}] Click 'Continue'")
                        await cont.click(force=True)
                        await page.wait_for_timeout(2000)
                except Exception:
                    break

            await clear_modals()

            page_content = await page.evaluate('''() => {
                const clone = (document.body || document.documentElement).cloneNode(true);
                const sidebarInClone = clone.querySelector('.sidebar-component');
                if (sidebarInClone) sidebarInClone.remove();

                const toRemove = clone.querySelectorAll('button, .badge, .continue-button, script, style, .self-closing-modal, .exercise-list');
                toRemove.forEach(c => c.remove());

                return clone.innerText;
            }''')

            results.append(
                {
                    "index": i,
                    "title": title_text,
                    "content": page_content.strip(),
                }
            )

            # Guardado incremental
            with output_file.open("w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            toggle = await page.query_selector("button#sidebar-toggle")
            if toggle:
                state = await toggle.get_attribute("data-state")
                if state == "closed":
                    await toggle.click(force=True)
                    await page.wait_for_timeout(1000)

        print(f"\nFinalizado tutorial {label}. Contenido guardado en {output_file}")
    finally:
        await page.close()


def slug_from_url(url: str) -> str:
    host = urlsplit(url).hostname or ""
    subdomain = host.split(".")[0] if host else "tutorial"
    slug = subdomain.replace("-", "_").strip("_")
    return slug or "tutorial"


def parse_target_spec(target_spec: str):
    if ":" not in target_spec:
        raise ValueError(f"Formato invalido en --target: '{target_spec}'. Usa class_x:url1,url2")

    class_name, raw_urls = target_spec.split(":", 1)
    class_name = class_name.strip()
    raw_urls = raw_urls.strip()

    if not class_name or not raw_urls:
        raise ValueError(f"Formato invalido en --target: '{target_spec}'. Usa class_x:url1,url2")

    if not re.match(r"^class_\d+$", class_name):
        raise ValueError(f"Nombre de clase invalido: '{class_name}'. Debe ser class_N")

    urls = [u.strip() for u in raw_urls.split(",") if u.strip()]
    if not urls:
        raise ValueError(f"No se encontraron URLs en --target: '{target_spec}'")

    return class_name, urls


def build_class_tutorials(target_specs):
    class_order = []
    class_configs = {}

    for target_spec in target_specs:
        class_name, urls = parse_target_spec(target_spec)
        if class_name not in class_configs:
            class_order.append(class_name)
            class_configs[class_name] = {
                "output_dir": BASE_DIR / class_name,
                "tutorials": [],
                "used_names": {},
            }

        class_config = class_configs[class_name]
        used_names = class_config["used_names"]

        for url in urls:
            base_name = slug_from_url(url)
            counter = used_names.get(base_name, 0) + 1
            used_names[base_name] = counter
            name = base_name if counter == 1 else f"{base_name}_{counter}"
            class_config["tutorials"].append({"name": name, "url": url})

    class_tutorials = []
    for class_name in class_order:
        class_config = class_configs[class_name]
        class_tutorials.append(
            {
                "output_dir": class_config["output_dir"],
                "tutorials": class_config["tutorials"],
            }
        )

    return class_tutorials


async def run(class_tutorials, max_concurrency: int):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )

        semaphore = asyncio.Semaphore(max_concurrency)

        async def scrape_with_limit(output_dir: Path, tutorial_name: str, url: str):
            async with semaphore:
                await scrape_tutorial(context, output_dir, tutorial_name, url)

        tasks = []
        for class_config in class_tutorials:
            output_dir = class_config["output_dir"]
            output_dir.mkdir(parents=True, exist_ok=True)
            for tutorial in class_config["tutorials"]:
                tasks.append((output_dir, tutorial["name"], tutorial["url"]))

        print(f"Iniciando scraping paralelo de {len(tasks)} tutorial(es) con max_concurrency={max_concurrency}")

        try:
            async with asyncio.TaskGroup() as tg:
                for output_dir, tutorial_name, url in tasks:
                    tg.create_task(scrape_with_limit(output_dir, tutorial_name, url))
        except* Exception as eg:
            first = eg.exceptions[0]
            raise RuntimeError(f"Scraping abortado por error: {first}") from first

        await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scraper de tutoriales LearnPack")
    parser.add_argument(
        "--target",
        dest="targets",
        action="append",
        required=True,
        help="Objetivo con formato class_x:url1,url2 (se puede repetir).",
    )
    parser.add_argument(
        "--max-concurrency",
        type=int,
        default=4,
        help="Numero maximo de tutoriales a procesar en paralelo (default: 4).",
    )
    args = parser.parse_args()

    if args.max_concurrency < 1:
        raise ValueError("--max-concurrency debe ser >= 1")

    selected = build_class_tutorials(args.targets)
    asyncio.run(run(selected, args.max_concurrency))
