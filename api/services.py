import re
from typing import List, Optional
from playwright.async_api import async_playwright, Page, Locator
from models import Production, Commercialization, Processing, Importing_or_Exporting
from utils import convert_numeric_string_to_float
from mappers import dictionary_processing_suboption_to_group, dictionary_importing_suboption_to_group, dictionary_exporting_suboption_to_group

# ITERADOR DE LÓGICA NO CASO DE PÁGINAS QUE TEM VÁRIAS ABAS
async def processing_iterator(page: Page, year: int, option: str):
    data = []
    number_iterations = len(dictionary_mapping_by_page[option])
    for i in range(1, 1 + number_iterations):
        data_for_subopt = await unique_iteration_processing(page, year, option, i)
        if data_for_subopt:
            data.extend(data_for_subopt)
    return data

# MÉTODO CHAMADO UMA VEZ INDIVIDUALMENTE (OU VÁRIAS VEZES PELO ITERADOR), PARA O PROCESSAMENTO COMUM E OS ESPECÍFICOS DE CADA PÁGINA
async def unique_iteration_processing(page: Page, year: int, option: str, subopt: Optional[int] = None):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao={option}"
    if subopt is not None:
        url = f"{url}&subopt=subopt_0{subopt}"

    try:
        await page.goto(url, timeout=40000, wait_until="domcontentloaded")
        await page.wait_for_selector("div.content_center", timeout=25000)
        valid_year = await get_year(page, year)
        # EXTRAÇÃO DOS DADOS DA TABELA
        div_data_table = page.locator("table.tb_base.tb_dados")
        div_body_data_table = div_data_table.locator("tbody")
        rows = await div_body_data_table.locator("tr").all()
        processed_data = await process_rows_by_option(option, rows, valid_year, subopt)
        return processed_data
    except Exception as e:
        raise e

# MÉTODO AUXILIAR QUE OBTÉM O ANO DA PÁGINA E EM CASO DE ERRO, UTILIZA O ANO INFORMADO MESMO
async def get_year(page: Page, year: int):
    div_content = page.locator("div.content_center")
    div_information = div_content.locator("p.text_center")
    text = await div_information.text_content()
    match = re.search(r"\[(\d{4})\]", text)
    return int(match.group(1)) if match else year

# EXECUTA O MÉTODO ESPECÍFICO DE CADA OPÇÃO/PÁGINA
async def process_rows_by_option(option: str, rows: List[Locator], year: int, subopt: Optional[int]):
    try:
        func = method_mapping_by_page[option]
        result = await func(rows, year,subopt)
        return result
    except KeyError:
        raise ValueError(f"Option '{option}' not implemented.")

async def process_production(rows: List[Locator], year: int, subopt: Optional[int]) -> List[Production]:
    productions: List[Production] = []
    last_category = ""
    last_quantity = 0
    count_itens_category = 0
    for row in rows:
        columns = row.locator("td")
        first_column = columns.nth(0)
        classes = await first_column.get_attribute("class")
        if classes == "tb_item":
            if(count_itens_category == 1):
                productions.append(
                Production(
                    category=last_category,
                    product=last_category.title(),
                    quantity=last_quantity,
                    unit="L",
                    measurement="volume",
                    year=year
                )
            )
            else:
                count_itens_category = 0
            count_itens_category = count_itens_category+1
            last_category = (await first_column.text_content()).strip()
            last_quantity = convert_numeric_string_to_float(await columns.nth(1).text_content())
        else:
            count_itens_category = 0
            product = (await first_column.text_content()).strip()
            quantity = convert_numeric_string_to_float(await columns.nth(1).text_content())
            productions.append(
                Production(
                    category=last_category,
                    product=product,
                    quantity=quantity,
                    unit="L",
                    measurement="volume",
                    year=year
                )
            )
    return productions

async def process_commercialization(rows: List[Locator], year: int, subopt: Optional[int]) -> List[Commercialization]:
    commercializations: List[Commercialization] = []
    last_category = ""
    last_quantity = 0
    count_itens_category = 0
    for row in rows:
        columns = row.locator("td")
        first_column = columns.nth(0)
        classes = await first_column.get_attribute("class")
        if classes == "tb_item":
            if(count_itens_category == 1):
                commercializations.append(
                Commercialization(
                    category=last_category,
                    product=last_category.title(),
                    quantity=last_quantity,
                    unit="L",
                    measurement="volume",
                    year=year
                )
            )
            else:
                count_itens_category = 0
            count_itens_category = count_itens_category+1
            last_category = (await first_column.text_content()).strip()
            last_quantity = convert_numeric_string_to_float(await columns.nth(1).text_content())
        else:
            count_itens_category = 0
            product = (await first_column.text_content()).strip()
            quantity = convert_numeric_string_to_float(await columns.nth(1).text_content())
            commercializations.append(
                Commercialization(
                    category=last_category,
                    product=product,
                    quantity=quantity,
                    unit="L",
                    measurement="volume",
                    year=year
                )
            )
    return commercializations

async def process_processing(rows: List[Locator], year: int, subopt: int) -> List[Processing]:
    group = dictionary_processing_suboption_to_group[subopt]
    processing: List[Processing] = []
    last_category = ""
    for row in rows:
        columns = row.locator("td")
        first_column = columns.nth(0)
        classes = await first_column.get_attribute("class")
        if classes == "tb_item":
            last_category = (await first_column.text_content()).strip()
        else:
            farm = (await first_column.text_content()).strip()
            quantity = convert_numeric_string_to_float(await columns.nth(1).text_content())
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

async def process_importing_or_exporting(rows: List[Locator], year: int, subopt: int) -> List[Importing_or_Exporting]:
    group = dictionary_importing_suboption_to_group[subopt]
    importing_or_exporting: List[Importing_or_Exporting] = []
    quantity = 0
    value = 0
    for row in rows:
        columns = row.locator("td")
        first_column = columns.nth(0)
        second_column = columns.nth(1)
        third_column = columns.nth(2)
        country = (await first_column.text_content()).strip()
        quantity = convert_numeric_string_to_float(await second_column.text_content())
        value = convert_numeric_string_to_float(await third_column.text_content())
        try:
            quantity = quantity
            value = value
        except:
            continue
        importing_or_exporting.append(
            Importing_or_Exporting(
                group=group,
                country=country,
                quantity=quantity,
                unit="Kg",
                measurement="mass",
                value=value,
                currency="US$",
                year=year
            )
        )
    return importing_or_exporting

# INICIALIZA O SCRAPING DE DADOS
async def run_scraping(year: int, option: str):
    browser = None
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            func = function_iterator[option]
            processed_data = await func(page, year, option)
            await browser.close()
            browser = None
            return processed_data
    except Exception as e:
        raise e
    finally:
        if browser and browser.is_connected():
            await browser.close()
            
# CORRELACIONAL O OPT_ PARA O DICIONÁRIO COM AS ABAS QUE ELE TEM
dictionary_mapping_by_page = {
    'opt_03': dictionary_processing_suboption_to_group,
    'opt_05': dictionary_importing_suboption_to_group,
    'opt_06': dictionary_exporting_suboption_to_group,
}

# MAPEAMENTO DE QUAL MÉTODO PRINCIPAL DEVE SER EXECUTADO POR CADA PÁGINA
method_mapping_by_page = {
    'opt_02': process_production,
    'opt_03': process_processing,
    'opt_04': process_commercialization,
    'opt_05': process_importing_or_exporting,
    'opt_06': process_importing_or_exporting
}

# MAPEAMENTO DE CADA PÁGINA PARA O RESPECTIVO MÉTODO RESPONSÁVEL POR GERENCIAR QUANTAS VEZES O MÉTODO PRINCIPAL DEVE SER CHAMADO (UMA PARA CADA ABA)
function_iterator = {
    'opt_02': unique_iteration_processing,
    'opt_03': processing_iterator,
    'opt_04': unique_iteration_processing,
    'opt_05': processing_iterator,
    'opt_06': processing_iterator,
}
