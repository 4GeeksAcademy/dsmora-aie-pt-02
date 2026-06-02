import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "class_09"

TUTORIALS = [
    {
        "name": "mastering_arrays_in_typescript",
        "url": "https://mastering-arrays-in-typescript.learn-pack.com#language=us&lang=us&theme=dark&iframe=true&token=5afa07602a4d20ea2641739587c1088d891ba710&cohort=1614&academy=6",
    },
]


async def scrape_tutorial(context, tutorial_name: str, url: str):
    page = await context.new_page()
    output_file = OUTPUT_DIR / f"{tutorial_name}.json"

    print(f"\n=== Tutorial: {tutorial_name} ===")
    print(f"Abriendo {url}...")

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
            print("Abriendo menu lateral...")
            await toggle.click(force=True)
            await page.wait_for_timeout(2000)

    cards = await page.query_selector_all("div.exercise-card")
    print(f"Se encontraron {len(cards)} lecciones.")

    results = []

    for i in range(len(cards)):
        await clear_modals()
        current_cards = await page.query_selector_all("div.exercise-card")
        if i >= len(current_cards):
            break
        card = current_cards[i]

        title_text = await card.inner_text()
        title_text = " ".join(title_text.split())
        print(f"\nProcesando leccion {i + 1}/{len(cards)}: {title_text}")

        await card.click(force=True)
        await page.wait_for_timeout(4000)

        # Intentar avanzar si aparecen bloqueos
        for _ in range(2):
            try:
                anyway = await page.get_by_role("button", name="Continue anyway").element_handle()
                if anyway and await anyway.is_visible():
                    print("  Click 'Continue anyway'")
                    await anyway.click(force=True)
                    await page.wait_for_timeout(2000)

                cont = await page.query_selector("div.continue-button")
                if cont and await cont.is_visible():
                    print("  Click 'Continue'")
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

    print(f"\nFinalizado tutorial {tutorial_name}. Contenido guardado en {output_file}")
    await page.close()


async def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        for tutorial in TUTORIALS:
            await scrape_tutorial(context, tutorial["name"], tutorial["url"])

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
