import re
from typing import List
from playwright.async_api import async_playwright, Page, Locator
from models import Production_or_Commercialization


async def get_processed_page_data(page: Page, year: int, option: str):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao={option}"
    await page.goto(url, timeout=40000, wait_until="domcontentloaded")
    await page.wait_for_selector("div.content_center", timeout=25000)
    valid_year = get_year(page, year)
    # Extração dos dados da tabela
    div_data_table = page.locator("table.tb_base.tb_dados")
    div_body_data_table = div_data_table.locator("tbody")
    rows = await div_body_data_table.locator("tr").all()
    process_rows_by_option(option, rows, valid_year)

async def get_year(page: Page, year: int):
    div_content = page.locator("div.content_center")
    div_information = div_content.locator("p.text_center")
    text = await div_information.text_content()
    match = re.search(r"\[(\d{4})\]", text)
    return int(match.group(1)) if match else year

async def process_rows_by_option(option: str, rows: List[Locator], year: int):
    try:
        func = dispatch_map[option]
    except KeyError:
        raise ValueError(f"Option '{option}' not implemented.")
    return await func(rows, year)

async def process_production_or_commercialization(rows: List[Locator], year: int) -> List[Production_or_Commercialization]:
    productions_or_commercialization: List[Production_or_Commercialization] = []
    last_category = ""
    for row in rows:
        columns = row.locator("td")
        first_collumn = columns.nth(0)
        classes = await first_collumn.get_attribute("class")
        if classes == "tb_item":
            last_category = (await first_collumn.text_content()).strip()
        else:
            product = (await first_collumn.text_content()).strip()
            str_value = (await columns.nth(1).text_content()).strip().replace(".", "").replace(",", "").replace("-","0")
            try:
                quantity = float(str_value)
            except:
                continue
            productions_or_commercialization.append(
                Production_or_Commercialization(
                    category=last_category,
                    product=product,
                    quantity=quantity,
                    unit="L",
                    measurement="volume",
                    year=year
                )
            )
    return productions_or_commercialization

dispatch_map = {
    'opt_02': process_production_or_commercialization,
    'opt_04': process_production_or_commercialization,
}


async def run_scraping(year: int, option):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        processed_data = await get_processed_page_data(page, year,option)
        await browser.close()
    return processed_data
