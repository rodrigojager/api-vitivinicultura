import re
import logging
from typing import List
from playwright.async_api import async_playwright, Page, Locator
from models import Production_or_Commercialization

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def get_processed_page_data(page: Page, year: int, option: str):
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano={year}&opcao={option}"
    logging.info(f"Navigating to URL: {url}")
    try:
        await page.goto(url, timeout=40000, wait_until="domcontentloaded")
        logging.info("Page loaded successfully.")
        await page.wait_for_selector("div.content_center", timeout=25000)
        logging.info("Content center found.")
        valid_year = await get_year(page, year) # Added await here
        logging.info(f"Validated year: {valid_year}")
        # Extração dos dados da tabela
        div_data_table = page.locator("table.tb_base.tb_dados")
        div_body_data_table = div_data_table.locator("tbody")
        rows = await div_body_data_table.locator("tr").all()
        logging.info(f"Found {len(rows)} rows in the table.")
        processed_data = await process_rows_by_option(option, rows, valid_year) # Added await and capture result
        logging.info("Finished processing rows.")
        return processed_data # Return the processed data
    except Exception as e:
        logging.exception(f"Error during page processing for URL {url}: {e}")
        raise # Re-raise the exception after logging

async def get_year(page: Page, year: int):
    div_content = page.locator("div.content_center")
    div_information = div_content.locator("p.text_center")
    text = await div_information.text_content()
    match = re.search(r"\[(\d{4})\]", text)
    return int(match.group(1)) if match else year

async def process_rows_by_option(option: str, rows: List[Locator], year: int):
    logging.info(f"Processing rows with option: {option}")
    try:
        func = dispatch_map[option]
        result = await func(rows, year)
        logging.info(f"Successfully processed {len(result)} items for option {option}.")
        return result
    except KeyError:
        logging.error(f"Option '{option}' not implemented.")
        raise ValueError(f"Option '{option}' not implemented.")
    except Exception as e:
        logging.exception(f"Error processing rows for option {option}: {e}")
        raise

async def process_production_or_commercialization(rows: List[Locator], year: int) -> List[Production_or_Commercialization]:
    logging.info("Starting process_production_or_commercialization")
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


async def run_scraping(year: int, option: str):
    logging.info(f"Starting scraping for year {year}, option {option}")
    processed_data = [] # Initialize in case of early error
    try:
        async with async_playwright() as p:
            logging.info("Launching browser...")
            browser = await p.chromium.launch(headless=True) # Consider adding args=['--no-sandbox'] if running as root in Docker
            page = await browser.new_page()
            logging.info("Browser launched, new page created.")
            processed_data = await get_processed_page_data(page, year, option)
            logging.info("Closing browser.")
            await browser.close()
        logging.info(f"Scraping finished successfully for year {year}, option {option}.")
        return processed_data
    except Exception as e:
        logging.exception(f"Error during scraping process for year {year}, option {option}: {e}")
        # Ensure browser is closed even if an error occurs before the context manager finishes
        try:
            if browser and browser.is_connected():
                await browser.close()
                logging.info("Browser closed after error.")
        except Exception as close_err:
            logging.error(f"Error closing browser after initial error: {close_err}")
        return processed_data # Return whatever was processed, or empty list
