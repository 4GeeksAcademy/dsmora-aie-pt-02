import asyncio
import json
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        # Tutorial: GitHub Fundamentals
        url = "https://github-fundamentals.learn-pack.com#language=es&lang=es&theme=dark&iframe=true&token=4160792f299f7888f15993a621ad9d8099b14b95&cohort=1613&academy=6"
        
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
                print("Abriendo menú lateral...")
                await toggle.click(force=True)
                await page.wait_for_timeout(2000)

        cards = await page.query_selector_all("div.exercise-card")
        print(f"Se encontraron {len(cards)} lecciones.")

        results = []

        for i in range(len(cards)):
            await clear_modals()
            current_cards = await page.query_selector_all("div.exercise-card")
            if i >= len(current_cards): break
            card = current_cards[i]
            
            title_text = await card.inner_text()
            title_text = " ".join(title_text.split())
            print(f"\nProcesando lección {i+1}/{len(cards)}: {title_text}")

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
                except: break

            await clear_modals()

            page_content = await page.evaluate('''() => {
                const sidebar = document.querySelector('.sidebar-component');
                const clone = (document.body || document.documentElement).cloneNode(true);
                const sidebarInClone = clone.querySelector('.sidebar-component');
                if (sidebarInClone) sidebarInClone.remove();
                
                const toRemove = clone.querySelectorAll('button, .badge, .continue-button, script, style, .self-closing-modal, .exercise-list');
                toRemove.forEach(c => c.remove());
                
                return clone.innerText;
            }''')

            results.append({
                "index": i,
                "title": title_text,
                "content": page_content.strip()
            })
            
            # Guardado incremental
            with open("tutorial_contents_v4.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            toggle = await page.query_selector("button#sidebar-toggle")
            if toggle:
                state = await toggle.get_attribute("data-state")
                if state == "closed":
                    await toggle.click(force=True)
                    await page.wait_for_timeout(1000)

        print(f"\nFinalizado. Contenido guardado en tutorial_contents_v4.json")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
