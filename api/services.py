import re
from typing import List, Optional
from playwright.async_api import async_playwright, Page, Locator
from models import Production_or_Commercialization, Processing

async def processing_iterator(page: Page, year: int, option: str):
    all_processing_data: List[Processing] = []
    for i in range(1, 5):
        data_for_subopt = await get_processed_page_data(page, year, option, i)
        if data_for_subopt:
            all_processing_data.extend(data_for_subopt)
    return all_processing_data

async def get_processed_page_data(page: Page, year: int, option: str, subopt: Optional[int] = None):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao={option}"
    if subopt is not None:
        url = f"{url}&subopt=subopt_0{subopt}"

    try:
        await page.goto(url, timeout=40000, wait_until="domcontentloaded")
        await page.wait_for_selector("div.content_center", timeout=25000)
        valid_year = await get_year(page, year)
        # Extração dos dados da tabela
        div_data_table = page.locator("table.tb_base.tb_dados")
        div_body_data_table = div_data_table.locator("tbody")
        rows = await div_body_data_table.locator("tr").all()
        processed_data = await process_rows_by_option(option, rows, valid_year, subopt)
        return processed_data
    except Exception as e:
        raise e

async def get_year(page: Page, year: int):
    div_content = page.locator("div.content_center")
    div_information = div_content.locator("p.text_center")
    text = await div_information.text_content()
    match = re.search(r"\[(\d{4})\]", text)
    return int(match.group(1)) if match else year

async def process_rows_by_option(option: str, rows: List[Locator], year: int, subopt: Optional[int]):
    try:
        func = dispatch_map[option]
        result = await func(rows, year,subopt)
        return result
    except KeyError:
        raise ValueError(f"Option '{option}' not implemented.")

async def process_production_or_commercialization(rows: List[Locator], year: int, subopt: Optional[int]) -> List[Production_or_Commercialization]:
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

async def process_processing(rows: List[Locator], year: int, subopt: int) -> List[Processing]:
    group = dictionary_processing_suboption_to_group[subopt]
    processing: List[Processing] = []
    last_category = ""
    for row in rows:
        columns = row.locator("td")
        first_collumn = columns.nth(0)
        classes = await first_collumn.get_attribute("class")
        if classes == "tb_item":
            last_category = (await first_collumn.text_content()).strip()
        else:
            farm = (await first_collumn.text_content()).strip()
            str_value = (await columns.nth(1).text_content()).strip().replace(".", "").replace(",", "").replace("-","0")
            try:
                quantity = float(str_value)
            except:
                continue
            processing.append(
                Processing(
                    group=group,
                    category=last_category,
                    farm=farm,
                    quantity=quantity,
                    unit="Kg",
                    measurement="mass",
                    year=year
                )
            )
    return processing

dictionary_processing_suboption_to_group = {
    1: "Viníferas",
    2: "Americanas e híbridas",
    3: "Uvas de mesa",
    4: "Sem classificação"
}

dispatch_map = {
    'opt_02': process_production_or_commercialization,
    'opt_03': process_processing,
    'opt_04': process_production_or_commercialization,
}

dispatch_map_iterator = {
    'opt_02': get_processed_page_data,
    'opt_03': processing_iterator,
    'opt_04': get_processed_page_data,
}


async def run_scraping(year: int, option: str):
    browser = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            func = dispatch_map_iterator[option]
            processed_data = await func(page, year, option)
            await browser.close()
            browser = None
            return processed_data
    except Exception as e:
        raise e
    finally:
        if browser and browser.is_connected():
            await browser.close()
