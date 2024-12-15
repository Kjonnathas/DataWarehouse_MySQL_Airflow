def sql_models() -> dict:
    """
    Retorna um dicionário com os modelos de dados e suas respectivas consultas SQL e campos.

    Este método encapsula as definições das tabelas dimensionais e fato utilizadas em um modelo star schema.
    Cada entrada do dicionário contém:
    - Nome do modelo (e.g., "dim_produto", "dim_cliente").
    - Consulta SQL associada à tabela.
    - Lista dos campos selecionados na consulta.

    Returns:
        dict: Dicionário onde as chaves representam o nome das tabelas e os valores incluem as seguintes informações:
            - "query_sql_<nome_tabela>": String com a consulta SQL.
            - "fields": Lista de strings representando os campos da tabela.

    Exemplo:
        O dicionário retornado tem a seguinte estrutura:
        {
            "dim_produto": {
                "query_sql_dim_produto": "SELECT ...",
                "fields": ["nk_produto", "produto", "modelo", "marca", "categoria", "subcategoria"]
            },
            "dim_cliente": {
                "query_sql_dim_cliente": "SELECT ...",
                "fields": ["nk_cliente", "nome_completo", "dt_nascimento", "idade", "genero"]
            },
            ...
        }
    """
    dict_models = {
        "dim_produto": {
            "query_sql_dim_produto": """
                    SELECT
                        produtos.id_produto AS nk_produto,
                        produtos.produto,
                        produtos.modelo,
                        marcas.marca,
                        categorias.categoria,
                        subcategorias.subcategoria
                    FROM
                        schema_staging.stg_tbl_produtos produtos,
                        schema_staging.stg_tbl_marcas marcas,
                        schema_staging.stg_tbl_subcategorias subcategorias,
                        schema_staging.stg_tbl_categorias categorias
                    WHERE
                        produtos.id_marca = marcas.id_marca AND
                        produtos.id_subcategoria = subcategorias.id_subcategoria AND
                        subcategorias.id_categoria = categorias.id_categoria;
                """,
            "fields": [
                "nk_produto",
                "produto",
                "modelo",
                "marca",
                "categoria",
                "subcategoria",
            ],
        },
        "dim_cliente": {
            "query_sql_dim_cliente": """
                    SELECT 
                        id_cliente AS nk_cliente,
                        nome || ' ' || sobrenome AS nome_completo,
                        dt_nascimento,
                        EXTRACT(YEAR FROM AGE(CURRENT_DATE, dt_nascimento))::INT AS idade,
                        genero
                    FROM 
                        schema_staging.stg_tbl_clientes;
                """,
            "fields": [
                "nk_cliente",
                "nome_completo",
                "dt_nascimento",
                "idade",
                "genero",
            ],
        },
        "dim_localidade": {
            "query_sql_dim_localidade": """
                    SELECT
                        localidades.id_endereco AS nk_localidade,
                        localidades.logradouro,
                        localidades.numero,
                        bairros.bairro,
                        cidades.cidade,
                        estados.estado,
                        estados.sigla_estado,
                        paises.pais,
                        localidades.cep
                    FROM
                        schema_staging.stg_tbl_enderecos localidades,
                        schema_staging.stg_tbl_bairros bairros,
                        schema_staging.stg_tbl_cidades cidades,
                        schema_staging.stg_tbl_estados estados,
                        schema_staging.stg_tbl_paises paises
                    WHERE
                        localidades.id_bairro = bairros.id_bairro AND
                        bairros.id_cidade = cidades.id_cidade AND
                        cidades.id_estado = estados.id_estado AND
                        estados.id_pais = paises.id_pais;
                """,
            "fields": [
                "nk_localidade",
                "logradouro",
                "numero",
                "bairro",
                "cidade",
                "estado",
                "sigla_estado",
                "pais",
                "cep",
            ],
        },
        "dim_tempo": {
            "query_sql_dim_tempo": """
                    SELECT
                        data::date,
                        EXTRACT(DAY FROM data) AS dia,
                        EXTRACT(MONTH FROM data) AS mes,
                        CASE
                            WHEN EXTRACT(MONTH FROM data) = 1 THEN 'Janeiro'
                            WHEN EXTRACT(MONTH FROM data) = 2 THEN 'Fevereiro'
                            WHEN EXTRACT(MONTH FROM data) = 3 THEN 'Março'
                            WHEN EXTRACT(MONTH FROM data) = 4 THEN 'Abril'
                            WHEN EXTRACT(MONTH FROM data) = 5 THEN 'Maio'
                            WHEN EXTRACT(MONTH FROM data) = 6 THEN 'Junho'
                            WHEN EXTRACT(MONTH FROM data) = 7 THEN 'Julho'
                            WHEN EXTRACT(MONTH FROM data) = 8 THEN 'Agosto'
                            WHEN EXTRACT(MONTH FROM data) = 9 THEN 'Setembro'
                            WHEN EXTRACT(MONTH FROM data) = 10 THEN 'Outubro'
                            WHEN EXTRACT(MONTH FROM data) = 11 THEN 'Novembro'
                            WHEN EXTRACT(MONTH FROM data) = 12 THEN 'Dezembro'
                        END AS mes_por_extenso,
                        EXTRACT(YEAR FROM data) AS ano,
                        SUBSTRING(EXTRACT(YEAR FROM data):: TEXT, 3, 2):: INT AS ano_abreviado,
                        CASE
                            WHEN TO_CHAR(data, 'D') = '1' THEN 'Domingo'
                            WHEN TO_CHAR(data, 'D') = '2' THEN 'Segunda-feira'
                            WHEN TO_CHAR(data, 'D') = '3' THEN 'Terça-feira'
                            WHEN TO_CHAR(data, 'D') = '4' THEN 'Quarta-feira'
                            WHEN TO_CHAR(data, 'D') = '5' THEN 'Quinta-feira'
                            WHEN TO_CHAR(data, 'D') = '6' THEN 'Sexta-feira'
                            WHEN TO_CHAR(data, 'D') = '7' THEN 'Sábado'
                        END AS dia_da_semana,
                        EXTRACT(WEEK FROM data) AS semana_do_ano,
                        CASE
                            WHEN EXTRACT(MONTH FROM data) IN (1, 2, 3) THEN 1
                            WHEN EXTRACT(MONTH FROM data) IN (4, 5, 6) THEN 2
                            WHEN EXTRACT(MONTH FROM data) IN (7, 8, 9) THEN 3
                            ELSE 4
                        END AS trimestre,
                        CASE
                            WHEN EXTRACT(MONTH FROM data) IN (1, 2, 3, 4, 5, 6) THEN 1
                            ELSE 2
                        END AS semestre,
                        CASE
                            WHEN TO_CHAR(data, 'FMDay') IN ('Saturday', 'Sunday') THEN 1
                            ELSE 0
                        END AS flag_final_de_semana,
                        CASE
                            WHEN TO_CHAR(data, 'FMDay') NOT IN ('Saturday', 'Sunday') THEN 1
                            ELSE 0
                        END AS flag_dia_util,
                        CASE
                            WHEN data IN 
                                ('2023-01-01', 
                                '2023-04-21', 
                                '2023-09-07', 
                                '2023-10-12', 
                                '2023-11-02', 
                                '2023-11-15', 
                                '2023-11-20', 
                                '2023-12-25', 
                                '2024-01-01', 
                                '2024-04-21', 
                                '2024-09-07', 
                                '2024-10-12', 
                                '2024-11-02', 
                                '2024-11-15', 
                                '2024-11-20', 
                                '2024-12-25') THEN 1
                            ELSE 0
                        END AS flag_feriado
                    FROM
                        GENERATE_SERIES('2023-01-01', '2024-12-31', INTERVAL '1' DAY) data;
                """,
            "fields": [
                "data",
                "dia",
                "mes",
                "mes_por_extenso",
                "ano",
                "ano_abreviado",
                "dia_da_semana",
                "semana_do_ano",
                "trimestre",
                "semestre",
                "flag_final_de_semana",
                "flag_dia_util",
                "flag_feriado",
            ],
        },
        "dim_loja": {
            "query_sql_dim_loja": """
                    SELECT
                        id_loja AS nk_loja,
                        loja
                    FROM
                        schema_staging.stg_tbl_lojas;
                """,
            "fields": ["nk_loja", "loja"],
        },
        "dim_canal_venda": {
            "query_sql_dim_canal_venda": """
                    SELECT
                        id_canal_venda AS nk_canal_venda,
                        canal_venda
                    FROM
                        schema_staging.stg_tbl_canal_vendas;
                """,
            "fields": ["nk_canal_venda", "canal_venda"],
        },
        "dim_vendedor": {
            "query_sql_dim_vendedor": """
                    SELECT 
                        id_funcionario AS nk_vendedor,
                        nome || ' ' || sobrenome AS nome_completo,
                        dt_nascimento,
                        EXTRACT(YEAR FROM AGE(CURRENT_DATE, dt_nascimento))::INT AS idade,
                        genero,
                        dt_admissao AS dt_contratacao
                    FROM 
                        schema_staging.stg_tbl_funcionarios;
                """,
            "fields": [
                "nk_vendedor",
                "nome_completo",
                "dt_nascimento",
                "idade",
                "genero",
                "dt_contratacao",
            ],
        },
        "fato_vendas_temp": {
            "query_sql_fato_vendas_temp": """
                    SELECT
                        vendas.id_produto,
                        vendas.id_funcionario AS id_vendedor,
                        vendas.id_cliente,
                        vendas.id_canal_venda,
                        pedidos.id_loja,
                        lojas.id_endereco AS id_localidade,
                        vendas.dt_venda,
                        vendas.id_venda as nk_venda,
                        vendas.qtde_itens_vendidos,
                        ROUND(vendas.valor_vendido, 2) AS valor_vendido,
                        ROUND(vendas.custo_total, 2) AS custo_total,
                        ROUND(vendas.desconto, 2) AS desconto,
                        ROUND((vendas.valor_vendido * (1 - vendas.desconto)) - vendas.custo_total, 2) AS lucro_total
                    FROM
                        schema_staging.stg_tbl_vendas vendas
                    LEFT JOIN
                        schema_staging.stg_tbl_pedidos pedidos ON vendas.id_pedido = pedidos.id_pedido
                    LEFT JOIN
                        schema_staging.stg_tbl_lojas lojas ON pedidos.id_loja = lojas.id_loja;
                """,
            "fields": [
                "id_produto",
                "id_vendedor",
                "id_cliente",
                "id_canal_venda",
                "id_loja",
                "id_localidade",
                "dt_venda",
                "nk_venda",
                "qtde_itens_vendidos",
                "valor_vendido",
                "custo_total",
                "desconto",
                "lucro_total",
            ],
        },
        "fato_vendas": {
            "query_sql_fato_vendas": """
                    SELECT
                        sk_produto,
                        sk_vendedor,
                        sk_cliente,
                        sk_canal_venda,
                        sk_loja,
                        sk_localidade,
                        sk_tempo,
                        nk_venda,
                        qtde_itens_vendidos,
                        valor_vendido,
                        custo_total,
                        desconto,
                        lucro_total
                    FROM (
                    SELECT
                        ROW_NUMBER() OVER (PARTITION BY produto.sk_produto, vendedor.sk_vendedor, cliente.sk_cliente, canal_venda.sk_canal_venda, loja.sk_loja, localidade.sk_localidade, tempo.sk_tempo, ft_vendas.nk_venda
                                            ORDER BY produto.sk_produto) AS rn,
                        produto.sk_produto,
                        vendedor.sk_vendedor,
                        cliente.sk_cliente,
                        canal_venda.sk_canal_venda,
                        loja.sk_loja,
                        localidade.sk_localidade,
                        tempo.sk_tempo,
                        ft_vendas.nk_venda,
                        ft_vendas.qtde_itens_vendidos,
                        ft_vendas.valor_vendido,
                        ft_vendas.custo_total,
                        ft_vendas.desconto,
                        ft_vendas.lucro_total
                    FROM
                        schema_dw.fato_vendas_temp ft_vendas
                    LEFT JOIN
                        schema_dw.dim_produto produto ON ft_vendas.id_produto = produto.nk_produto
                    LEFT JOIN
                        schema_dw.dim_vendedor vendedor ON ft_vendas.id_vendedor = vendedor.nk_vendedor
                    LEFT JOIN
                        schema_dw.dim_cliente cliente ON ft_vendas.id_cliente = cliente.nk_cliente
                    LEFT JOIN
                        schema_dw.dim_canal_venda canal_venda ON ft_vendas.id_canal_venda = canal_venda.nk_canal_venda
                    LEFT JOIN
                        schema_dw.dim_loja loja ON ft_vendas.id_loja = loja.nk_loja
                    LEFT JOIN
                        schema_dw.dim_localidade localidade ON ft_vendas.id_localidade = localidade.nk_localidade
                    LEFT JOIN
                        schema_dw.dim_tempo tempo ON ft_vendas.dt_venda = tempo.data
                    LIMIT 200000
                    )
                    WHERE
                        rn = 1;
                """,
            "fields": [
                "sk_produto",
                "sk_vendedor",
                "sk_cliente",
                "sk_canal_venda",
                "sk_loja",
                "sk_localidade",
                "sk_tempo",
                "nk_venda",
                "qtde_itens_vendidos",
                "valor_vendido",
                "custo_total",
                "desconto",
                "lucro_total",
            ],
        },
    }

    return dict_models
