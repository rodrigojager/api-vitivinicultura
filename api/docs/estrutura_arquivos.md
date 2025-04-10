# Estrutura dos arquivos

Nessa página vamos explicar a organização e funcionalidade dos arquivos

## main_api.py

Responsável por criar e inicializar banco de dados e tabela de usuários, inicializar apis com endpoints e definir rotas de navegação.

## services.py

O arquivo `services.py` contém a lógica de negócios da API, responsável por realizar o scraping e processamento de dados relacionados à produção, processamento, comercialização, importação e exportação de uvas e seus derivados. Ele utiliza a biblioteca Playwright para acessar páginas da web e extrair informações relevantes.

### Funções Principais

#### 1. `run_scraping(year: int, option: str)`

Esta função é a entrada principal para iniciar o processo de scraping. Ela recebe um ano e uma opção que determina qual tipo de dados será coletado.

##### Parâmetros

- **year**: Ano de referência para o scraping.
- **option**: Opção que determina qual tipo de dados será coletado.

##### Funcionamento

- A função inicializa um navegador headless usando Playwright.
- Chama a função correspondente ao tipo de dados a ser coletado, utilizando a opção fornecida.
- Retorna os dados processados.

#### 2. `processing_iterator(page: Page, year: int, option: str)`

Esta função itera sobre as páginas que contêm dados, chamando a função de processamento apropriada para cada aba.

##### Parâmetros

- **page**: A página do navegador onde o scraping está sendo realizado.
- **year**: Ano de referência.
- **option**: Opção que determina qual tipo de dados será coletado.

##### Funcionamento

- A função determina quantas iterações são necessárias com base na opção fornecida.
- Para cada iteração, chama a função `unique_iteration_processing`.

#### 3. `unique_iteration_processing(page: Page, year: int, option: str, subopt: Optional[int] = None)`

Esta função é responsável por processar uma única iteração de scraping.

##### Parâmetros

- **page**: A página do navegador.
- **year**: Ano de referência.
- **option**: Opção que determina qual tipo de dados será coletado.
- **subopt**: Subopção para páginas que têm várias abas (opcional).

##### Funcionamento

- A função constrói a URL com base no ano e na opção.
- Acessa a URL e aguarda o carregamento do conteúdo.
- Extrai os dados da tabela e chama a função de processamento apropriada.

#### 4. `process_rows_by_option(option: str, rows: List[Locator], year: int, subopt: Optional[int])`

Esta função processa as linhas da tabela de dados com base na opção fornecida.

##### Parâmetros

- **option**: Opção que determina qual tipo de dados será coletado.
- **rows**: Linhas da tabela a serem processadas.
- **year**: Ano de referência.
- **subopt**: Subopção para páginas que têm várias abas (opcional).

##### Funcionamento

- A função chama a função de processamento específica com base na opção.
- Retorna os dados processados.

#### 5. Funções de Processamento Específicas

Existem várias funções específicas para processar diferentes tipos de dados, como `process_production_or_commercialization`, `process_processing`, e `process_importing_or_exporting`. Cada uma dessas funções é responsável por extrair e formatar os dados de acordo com a estrutura definida nas classes de modelo.

## models.py

Contém modelos usando a biblioteca `pydantic`, para estruturar os dados retornados pela api e facilitar a estruturação do retorno pelo Swagger UI, incluindo tipagem e exemplos dos dados de cada retorno. Mais detalhes dos models estão presentes na seção **Modelos de Dados**

## mappers.py

Dicionários que mapeiam condições de fluxos ou opções dos métodos de acordo com as páginas que serão "raspadas".

## auth.py

Métodos de geração e validação de credenciais e tokes jwt.

## utils.py

Métodos para facilitar o processamento de dados, como conversão de uma string numérica para um valor númerico.