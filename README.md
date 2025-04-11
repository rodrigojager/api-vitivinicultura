# Bem-vindo à Documentação da API 

Esta API serve como um serviço de backend para gerenciar informações sobre a produção, processamento, comercialização, importação e exportação de uvas e seus derivados no Estado do Rio Grande do Sul. Ela fornece um conjunto de endpoints que permitem que os clientes interajam com os dados e realizem operações específicas.

A documentação completa, junto com a API está disponível em: [https://jager.lat](https://jager.lat)

## Introdução

Os dados retornados pela API são obtidos através de scraping utilizando a biblioteca playwright que executa a ação no momento da requisição. Antes de começar a utilizar a API, voce precisa se Registrar em /registration

## Motivação

O desenvolvimento dessa solução visa atender ao Tech Challenge Fase 01 do curso de Machine Learning Engineering da FIAP.

## Requisitos

- Criar uma Rest API em Python que faça a consulta no site da Embrapa e retorne dados de Produção, Processamento, Comercialização, Importação e Exportação.
- API deve ser documentada
- É recomendável (não obrigatório) a escolha de um método de autenticação.
- Criar um plano para fazer o deploy da API, desenhando a arquitetura do projeto desde a ingestão até a alimentação do modelo (não é necessário elaborar um modelo de ML, mas é preciso que vocês escolham um cenário interessante em que a API possa ser utilizada).
- Fazer um MVP realizando o deploy com um link compartilhável e um repositório no github.

## Estruturação da Solução

A solução foi implementada através de containers dockers para encapsular os requisitos e rodar de maneira consistente e padronizada em qualquer ambiente. Existem basicamente 2 containers. O primeiro é um banco de dados em Postgress, utilizado para armazenar credenciais dos usuários. O segundo container hospeda a API com FastAPI e sua respectiva documentação em Swagger UI e a documentação adicional usando MkDocs (essa que você está visualizando). Existe ainda uma outra documentação padrão fornecida pela FastAPI que é o Redoc que está ativa no endereço /redoc, mas por considerar inferior tanto ao Swagger UI, quanto ao MkDocs, não será considerado nessa documentação ou nos menus.

O MKDocs é um interpretador de documentos markdown que gera uma visualização estruturada e conta com diversos plugins e temas para melhorar a experiência de leitura da documentação.

A API exige autenticação de usuários utilizando JWT, então ela se conecta ao banco de dados para validar as credenciais.

O usuário autenticado pode usar os endpoints para iniciar o scraping de dados ao site de [vitivinicultura da Embrapa](http://vitibrasil.cnpuv.embrapa.br/). Nesse momento, o Playwright é inicializado e navega para a página em modo headless (invisível para o usuário), obtendo os dados e retornando-os de maneira estruturada. Embora existam outras bibliotecas populares capazes de fazer webscraping como o Selenium e o Puppeteer, o Playwright vem se mostrando mais eficiente que o primeiro e relativamente mais popular que o segundo e por isso foi a opção escolhida.
