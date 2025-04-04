import re
from typing import List
from playwright.async_api import async_playwright, Page
from models import Production

async def fetch_productions(page: Page, ano: int) -> List[Production]:
    productions: List[Production] = []
    # Navega para a página
    url = f"http://vitibrasil.cnpuv.embrapa.br/index.php?ano=2016&opcao=opt_02"
    await page.goto(url, timeout=40000, wait_until="domcontentloaded")
    
    # Verifica se o elemento chave existe
    await page.wait_for_selector("div.content_center", timeout=25000)
    
    # Extração do ano da página
    div_conteudo = page.locator("div.content_center")
    div_informacao = div_conteudo.locator("p.text_center")
    texto = await div_informacao.text_content()
    match = re.search(r"\[(\d{4})\]", texto)
    ano_producao = int(match.group(1)) if match else ano

    # Extração dos dados da tabela
    div_tabela_dados = page.locator("table.tb_base.tb_dados")
    div_body_tabela_dados = div_tabela_dados.locator("tbody")
    ultima_categoria = ""
    rows = await div_body_tabela_dados.locator("tr").all()
    for row in rows:
        colunas = row.locator("td")
        primeira_coluna = colunas.nth(0)
        classe = await primeira_coluna.get_attribute("class")
        if classe == "tb_item":
            ultima_categoria = (await primeira_coluna.text_content()).strip()
        else:
            produto = (await primeira_coluna.text_content()).strip()
            valor_str = (await colunas.nth(1).text_content()).strip().replace(".", "").replace(",", "").replace("-","0")
            try:
                quantidade = float(valor_str)
            except:
                continue
            productions.append(
                Production(
                    category=ultima_categoria,
                    product=produto,
                    quantity=quantidade,
                    unit="L",
                    measurement="volume",
                    year=ano_producao
                )
            )
    return productions

async def run_scraping(ano: int) -> List[Production]:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        productions = await fetch_productions(page, ano)
        await browser.close()
    return productions

