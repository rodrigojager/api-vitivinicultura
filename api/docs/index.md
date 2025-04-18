# Bem-vindo à Documentação do Projeto 

Este projeto traz uma API que serve como um serviço de backend para gerenciar informações sobre a produção, processamento, comercialização, importação e exportação de uvas e seus derivados no Estado do Rio Grande do Sul. Ela fornece um conjunto de endpoints que permitem que os clientes interajam com os dados e realizem operações específicas.

A solução está disponível no GitHub do desenvolvedor: [API Vitivinicultura no GitHub]https://github.com/rodrigojager/api-vitivinicultura

## Introdução

Os dados retornados pela API são obtidos através de scraping utilizando a biblioteca playwright que executa a ação no momento da requisição. Antes de começar a utilizar a API, voce precisa se [Registrar](/registration)

## Motivação

O desenvolvimento dessa solução visa atender ao Tech Challenge Fase 01 do curso de Machine Learning Engineering da FIAP.

## Requisitos

- Criar uma Rest API em Python que faça a consulta no site da Embrapa e retorne dados de Produção, Processamento, Comercialização, Importação e Exportação.
- API deve ser documentada
- É recomendável (não obrigatório) a escolha de um método de autenticação.
- Criar um plano para fazer o deploy da API, desenhando a arquitetura do projeto desde a ingestão até a alimentação do modelo (não é necessário elaborar um modelo de ML, mas é preciso que vocês escolham um cenário interessante em que a API possa ser utilizada).
- Fazer um MVP realizando o deploy com um link compartilhável e um repositório no github.

## Estruturação da Solução

A solução foi implementada através de containers dockers para encapsular os requisitos e rodar de maneira consistente e padronizada em qualquer ambiente. Existem basicamente 2 containers. O primeiro é um banco de dados em Postgress, utilizado para armazenar credenciais dos usuários. O segundo container hospeda a API com FastAPI e sua respectiva documentação em Swagger UI e a documentação adicional usando MkDocs (essa que você está visualizando). Existe ainda uma outra documentação padrão fornecida pela FastAPI que é o Redoc que está ativa no endereço [/redoc](/redoc), mas por considerar inferior tanto ao Swagger UI, quanto ao MkDocs, não será considerado nessa documentação ou nos menus.

O MKDocs é um interpretador de documentos markdown que gera uma visualização estruturada e conta com diversos plugins e temas para melhorar a experiência de leitura da documentação.

A API exige autenticação de usuários utilizando JWT, então ela se conecta ao banco de dados para validar as credenciais.

O usuário autenticado pode usar os endpoints para iniciar o scraping de dados ao site de [vitivinicultura da Embrapa](http://vitibrasil.cnpuv.embrapa.br/). Nesse momento, o Playwright é inicializado e navega para a página em modo headless (invisível para o usuário), obtendo os dados e retornando-os de maneira estruturada. Embora existam outras bibliotecas populares capazes de fazer webscraping como o Selenium e o Puppeteer, o Playwright vem se mostrando mais eficiente que o primeiro e relativamente mais popular que o segundo e por isso foi a opção escolhida.

## Estrutura da documentação

- Apresentação: Essa página de apresentação do projeto
- Arquitetura do Projeto: Uma explicação de como está estruturada a infraestrutura da publicação da solução
- Documentação da API: Documentação da api com seus endpoints e fluxos de uso
- Fluxo de Scraping: Explicação de como foi feito o scraping e desenvolvimento do código por trás da API.
- Modelos de Dados: Apresentação dos modelos utilizados para armazenar os dados retornados pelos endpoints e da estrutura do banco de dados (que é responsável apenas por armazenar dados das credenciais dos usuários).
- Estrutura dos Arquivos: Descrição analítica da funcionalidade de cada arquivo desenvolvido e uma breve descrição dos seus métodos e dicionários/mapas.

## Utilidade da API

- A API fornece os dados mais atualizados de cada ano de produção, processamento, importação, exportação e comercialização de uva e derivados do Rio Grande do Sul. Na posse desses dados, um desenvolvedor pode por exemplo utilizar de machine learning para fazer predições, podendo auxiliar um empresário do ramo a otimizar o controle de estoque, de produção, de caixa financeiro e ações de marketing de produtos para países com base nas exportações.