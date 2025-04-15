# Modelos de Dados

## Modelos

!!! warning "Atenção"
    Como os retornos são iguais para algumas páginas, em alguns casos isso resultou em uma única classe para 2 páginas diferentes. Essa abordagem foi feita pensando em seguir o princípio DRY (Don't Repeat Yourself), ainda que isso viole os princípios OCP (Open-closed principle) e o SRP (Single Responsability Principle) do **SO**LID. Essa escolha deliberada visa simplificar o código e como aqui está sendo utilizado apenas para fins acadêmicos, não foi considerada prejudicial para o resultado final.

### 1. `Production`

Esta classe representa os dados relacionados à produção de derivados de uva. 

#### Atributos
- **category**: Categoria do produto (ex: VINHO DE MESA).
- **product**: Tipo do produto (ex: Tinto).
- **quantity**: Quantidade anual (ex: 103916391).
- **unit**: Unidade de medida (ex: L).
- **measurement**: Grandeza medida (ex: volume).
- **year**: Ano de referência (ex: 2020).

### 2. `Commercialization`

Esta classe representa os dados relacionados à comercialização de produtos derivados de uva. 

#### Atributos
- **category**: Categoria do produto (ex: VINHO DE MESA).
- **product**: Tipo do produto (ex: Tinto).
- **quantity**: Quantidade anual (ex: 103916391).
- **unit**: Unidade de medida (ex: L).
- **measurement**: Grandeza medida (ex: volume).
- **year**: Ano de referência (ex: 2020).

### 3. `Processing`
Esta classe representa os dados relacionados ao processamento de uvas.

#### Atributos
- **group**: Grupo da uva (ex: Viníferas).
- **category**: Categoria do cultivo (ex: TINTAS).
- **farm**: Casta de cultivo (ex: TIAlicante Bouschet).
- **quantity**: Quantidade anual (ex: 2272985).
- **unit**: Unidade de medida (ex: Kg).
- **measurement**: Grandeza medida (ex: mass).
- **year**: Ano de referência (ex: 2020).

### 4. `Importing_or_Exporting`
Esta classe representa os dados relacionados à importação ou exportação de produtos derivados de uva.

#### Atributos
- **group**: Grupo de derivados de uva (ex: Vinhos de mesa).
- **country**: País comercializante (ex: Alemanha).
- **quantity**: Quantidade comercializada (ex: 136992).
- **unit**: Unidade de medida (ex: Kg).
- **measurement**: Grandeza medida (ex: mass).
- **value**: Valor transacionado (ex: 504168).
- **currency**: Moeda (ex: US$).
- **year**: Ano de referência (ex: 2020).



# Estrutura do Banco de Dados

Foi criado um servidor Postgress rodando dentro do container. Nesse servidor, temos o banco de dados chamado users_api, com a tabela users para guardar os usuários criados para uso da API. As senhas do usuário são *hasheadas* com bcrypt, usando salt e armazenadas no banco de dados

## Tabela de Usuários

A tabela de usuários é responsável por armazenar as informações de registro dos usuários que utilizarão a API. A estrutura da tabela é a seguinte:

| Campo             | Tipo                       | Descrição                                        |
| ----------------- | -------------------------- | ------------------------------------------------ |
| **id**            | Integer (PK)               | Identificador único do usuário auto incremental. |
| **username**      | Character varying (Unique) | Nome de usuário único.                           |
| **password_hash** | Character varying          | Hash da senha do usuário.                        |
| **created_at**    | Timestap without time zone | Data e hora de criação do registro.              |
