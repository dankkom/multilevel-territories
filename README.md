# TABELA DIMENSÃO DE GEOGRAFIA

Contém:

- Código da Unidade Territorial
- Unidade Territorial, que inclui:
    - Municípios brasileiros segundo o IBGE (nome e código). Os nomes dos municípios foram concatenados com a sigla da Unidade da Federação (UF), separado com " - ", para evitar duplicidades em diferentes UFs.
    - Microrregiões segundo o IBGE (nome e código).
    - Mesorregiões segundo o IBGE (nome e código).
    - Regiões Metropolitanas (RM) segundo o IBGE (nome e código). Os nomes das RMs foram concatenados com a sigla da Unidade da Federação (UF), separado com " - ", para seguir o padrão de nomenclatura no SIDRA.
    - Grandes Regiões segundo o IBGE.
    - Países segundo o IBGE e a Organização das Nações Unidas (ONU).
- Nível Territorial, que inclui:
    - Município
    - Microrregião
    - Mesorregião
    - Região Metropolitana
    - País

Exceto pelas RMs e Países, os códigos originais foram mantidos.

Os códigos das RMs, para evitar colisão com os códigos das mesorregiões, foram multiplicados por 10.000.

Os códigos M49 dos Países, para evitar colisão com os códigos do IBGE, foram multiplicados por -1.


## Como usar:

Instalar as dependências:

```sh
pipenv install
```

Executar script `get_ibge_rm_ride.py` para baixar os dados de Regiões Metropolitanas do IBGE.

```sh
pipenv run python get_ibge_rm_ride.py
```

Executar script `get_geografia.py` para baixar dados de municípios e países do IBGE e montar a tabela final com os dados, gravando no arquivo `data-output/d_geografia.csv`.

```sh
pipenv run python get_geografia.py
```

Importar os dados do arquivo `data-output/d_geografia.csv` para um banco de dados.
