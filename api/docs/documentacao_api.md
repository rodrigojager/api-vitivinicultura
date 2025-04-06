# Documentação da API

## Endpoints Principais

- **POST /login**: Autentica um usuário e retorna um token de acesso.
- **GET /production**: Retorna dados sobre a produção de vinhos, sucos e derivados.
- **GET /processing**: Retorna a quantidade de uvas processadas.
- **GET /commercialization**: Retorna dados sobre a comercialização de vinhos e derivados.
- **GET /importing**: Retorna dados sobre a importação de derivados de uva.
- **GET /exporting**: Retorna dados sobre a exportação de derivados de uva.



## Fluxo de uso da API

Uma vez que voce já tenha se [registrado](/registration), você precisa obter um **token** de autenticação tipo **Bearer** e utilizar esse token para todas as requisições subsequentes. Faça um **POST** para o endpoint **<u>/login</u>** com seu nome de usuário e senha. Como resposta voce terá o Bearer token.

Em posse do token, voce pode proceder com a requisição aos demais endpoints, passando via **GET** o ano do qual voce deseja obter os dados.

![fluxo_api](C:\Users\Rodrigo\Desktop\Pós Machine Learning\api-vitivinicultura\api\docs\images\fluxo_api.svg)



## Detalhes dos Endpoints

### 1. POST /login

#### Descrição
Autentica um usuário e retorna um token de acesso.

#### Parâmetros
- **username**: Nome de usuário (string, obrigatório).
- **password**: Senha do usuário (string, obrigatório).

#### Exemplo de Requisição
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=usuario_exemplo&password=senha_exemplo
```

#### Exemplo de Resposta
```json
{
  "access_token": "token_de_acesso",
  "token_type": "bearer"
}
```

### 2. GET /production
#### Descrição
Retorna dados sobre a produção de vinhos, sucos e derivados.

#### Parâmetros
- **year**: Ano de referência (integer, obrigatório).

#### Exemplo de Requisição
```http
GET /production?year=2020
Authorization: Bearer token_de_acesso
```

#### Exemplo de Resposta
```json
[
  {
    "category": "VINHO DE MESA",
    "product": "Tinto",
    "quantity": 103916391,
    "unit": "L",
    "measurement": "volume",
    "year": 2020
  }
]
```

### 3. GET /processing
#### Descrição
Retorna a quantidade de uvas processadas.

#### Parâmetros
- **year**: Ano de referência (integer, obrigatório).

#### Exemplo de Requisição
```http
GET /processing?year=2020
Authorization: Bearer token_de_acesso
```

#### Exemplo de Resposta
```json
[
  {
    "group": "Viníferas",
    "category": "TINTAS",
    "farm": "TIAlicante Bouschet",
    "quantity": 2272985,
    "unit": "Kg",
    "measurement": "mass",
    "year": 2020
  }
]
```

### 4. GET /commercialization
#### Descrição
Retorna dados sobre a comercialização de vinhos e derivados.

#### Parâmetros
- **year**: Ano de referência (integer, obrigatório).

#### Exemplo de Requisição
```http
GET /commercialization?year=2020
Authorization: Bearer token_de_acesso
```

#### Exemplo de Resposta
```json
[
  {
    "category": "VINHO DE MESA",
    "product": "Tinto",
    "quantity": 50000,
    "unit": "L",
    "measurement": "volume",
    "year": 2020
  }
]
```

### 5. GET /importing
#### Descrição
Retorna dados sobre a importação de derivados de uva.

#### Parâmetros
- **year**: Ano de referência (integer, obrigatório).

#### Exemplo de Requisição
```http
GET /importing?year=2020
Authorization: Bearer token_de_acesso
```

#### Exemplo de Resposta
```json
[
  {
    "group": "Vinhos de mesa",
    "country": "Alemanha",
    "quantity": 136992,
    "unit": "Kg",
    "measurement": "mass",
    "value": 504168,
    "currency": "US$",
    "year": 2020
  }
]
```

### 6. GET /exporting
#### Descrição
Retorna dados sobre a exportação de derivados de uva.

#### Parâmetros
- **year**: Ano de referência (integer, obrigatório).

#### Exemplo de Requisição
```http
GET /exporting?year=2020
Authorization: Bearer token_de_acesso
```

#### Exemplo de Resposta
```json
[
  {
    "group": "Vinhos de mesa",
    "country": "França",
    "quantity": 50000,
    "unit": "Kg",
    "measurement": "mass",
    "value": 300000,
    "currency": "US$",
    "year": 2020
  }
]

```
