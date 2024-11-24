def tables_config() -> dict:
    dict_tables_config = {
        "tbl_canal_vendas": {
            "schema": """
                id_canal_venda INTEGER AUTO_INCREMENT,
                canal_venda VARCHAR (15) NOT NULL,
                CONSTRAINT tbl_canal_vendas_id_canal_venda_pk PRIMARY KEY (id_canal_venda)
            """,
            "csv_file": "tbl_canal_vendas.csv",
            "columns": ["canal_venda"],
        },
        "tbl_status_pagamentos": {
            "schema": """
                id_status_pagamento INTEGER AUTO_INCREMENT,
                status_pagamento VARCHAR (20) NOT NULL,
                CONSTRAINT tbl_status_pgto_id_status_pgto_pk PRIMARY KEY (id_status_pagamento)
            """,
            "csv_file": "tbl_status_pagamento.csv",
            "columns": ["status_pagamento"],
        },
        "tbl_forma_pagamentos": {
            "schema": """
                id_forma_pagamento INTEGER AUTO_INCREMENT,
                tipo_forma_pagamento VARCHAR (20) NOT NULL,
                CONSTRAINT tbl_forma_pgto_id_forma_pgto_pk PRIMARY KEY (id_forma_pagamento)
            """,
            "csv_file": "tbl_forma_pagamentos.csv",
            "columns": ["tipo_forma_pagamento"],
        },
        "tbl_status_pedidos": {
            "schema": """
                id_status_pedido INTEGER AUTO_INCREMENT,
                status_pedido VARCHAR (50) NOT NULL,
                CONSTRAINT tbl_status_ped_id_status_ped_pk PRIMARY KEY (id_status_pedido)
            """,
            "csv_file": "tbl_status_pedidos.csv",
            "columns": ["status_pedido"],
        },
        "tbl_referencias": {
            "schema": """
                id_referencia INTEGER AUTO_INCREMENT,
                tipo_referencia VARCHAR (20) NOT NULL,
                CONSTRAINT tbl_ref_id_ref_pk PRIMARY KEY (id_referencia)
            """,
            "csv_file": "tbl_referencias.csv",
            "columns": ["tipo_referencia"],
        },
        "tbl_paises": {
            "schema": """
                id_pais INTEGER AUTO_INCREMENT,
                pais VARCHAR (50) NOT NULL,
                CONSTRAINT tbl_paises_id_pais_pk PRIMARY KEY (id_pais)
            """,
            "csv_file": "tbl_paises.csv",
            "columns": ["pais"],
        },
        "tbl_estados": {
            "schema": """
                id_estado INTEGER AUTO_INCREMENT,
                id_pais INTEGER NOT NULL,
                estado VARCHAR (50) NOT NULL,
                sigla_estado CHAR (2) NOT NULL,
                CONSTRAINT tbl_estados_id_estado_pk PRIMARY KEY (id_estado),
                CONSTRAINT tbl_estados_id_pais_fk FOREIGN KEY (id_pais) REFERENCES tbl_paises (id_pais)
            """,
            "csv_file": "tbl_estados.csv",
            "columns": ["id_pais", "estado", "sigla_estado"],
        },
        "tbl_cidades": {
            "schema": """
                id_cidade INTEGER AUTO_INCREMENT,
                id_estado INTEGER NOT NULL,
                cidade VARCHAR (50) NOT NULL,
                CONSTRAINT tbl_cidades_id_cidade_pk PRIMARY KEY (id_cidade),
                CONSTRAINT tbl_cidades_id_estado_fk FOREIGN KEY (id_estado) REFERENCES tbl_estados (id_estado)
            """,
            "csv_file": "tbl_cidades.csv",
            "columns": ["id_estado", "cidade"],
        },
        "tbl_bairros": {
            "schema": """
                id_bairro INTEGER AUTO_INCREMENT,
                id_cidade INTEGER NOT NULL,
                bairro VARCHAR (100) NOT NULL,
                CONSTRAINT tbl_cidades_id_bairro_pk PRIMARY KEY (id_bairro),
                CONSTRAINT tbl_cidades_id_cidade_fk FOREIGN KEY (id_cidade) REFERENCES tbl_cidades (id_cidade)
            """,
            "csv_file": "tbl_bairros.csv",
            "columns": ["id_cidade", "bairro"],
        },
        "tbl_enderecos": {
            "schema": """
                id_endereco INTEGER AUTO_INCREMENT,
                id_referencia INTEGER NOT NULL,
                id_bairro INTEGER NOT NULL,
                logradouro VARCHAR (100) NOT NULL,
                numero INTEGER NOT NULL,
                cep VARCHAR (20) NOT NULL,
                CONSTRAINT tbl_end_id_end_pk PRIMARY KEY (id_endereco),
                CONSTRAINT tbl_end_id_ref_fk FOREIGN KEY (id_referencia) REFERENCES tbl_referencias (id_referencia),
                CONSTRAINT tbl_end_id_bairro_fk FOREIGN KEY (id_bairro) REFERENCES tbl_bairros (id_bairro)
            """,
            "csv_file": "tbl_enderecos.csv",
            "columns": ["id_referencia", "id_bairro", "logradouro", "numero", "cep"],
        },
        "tbl_tipos_contatos": {
            "schema": """
                id_tipo_contato INTEGER AUTO_INCREMENT,
                tipo_contato VARCHAR (30) NOT NULL,
                CONSTRAINT tbl_tipos_contatos_id_tipo_contato_pk PRIMARY KEY (id_tipo_contato)
            """,
            "csv_file": "tbl_tipos_contatos.csv",
            "columns": ["tipo_contato"],
        },
        "tbl_contatos": {
            "schema": """
                id_contato INTEGER AUTO_INCREMENT,
                id_tipo_contato INTEGER NOT NULL,
                id_referencia INTEGER NOT NULL,
                telefone VARCHAR (13) NOT NULL,
                email VARCHAR (50) NOT NULL,
                status_contato CHAR (1) NOT NULL,
                CONSTRAINT tbl_contatos_id_contato_pk PRIMARY KEY (id_contato),
                CONSTRAINT tbl_contatos_id_tipo_contato_fk FOREIGN KEY (id_tipo_contato) REFERENCES tbl_tipo_contatos (id_tipo_contato),
                CONSTRAINT tbl_contatos_id_ref_fk FOREIGN KEY (id_referencia) REFERENCES tbl_referencias (id_referencia),
                CONSTRAINT tbl_contatos_telefone_ck CHECK (id_tipo_contato IN (1, 2, 3) AND telefone NOT LIKE '%@%'),
                CONSTRAINT tbl_contatos_email_ck CHECK (id_tipo_contato = 4 AND email LIKE '%@%')
            """,
            "csv_file": "tbl_contatos.csv",
            "columns": [
                "id_tipo_contato",
                "id_referencia",
                "telefoe",
                "email",
                "status_contato",
            ],
        },
        "tbl_clientes": {
            "schema": """
                id_cliente INTEGER AUTO_INCREMENT,
                id_contato INTEGER NOT NULL,
                id_endereco INTEGER NOT NULL,
                nome VARCHAR (50) NOT NULL,
                sobrenome VARCHAR (100) NOT NULL,
                dt_nascimento DATE NOT NULL,
                genero CHAR (1),
                cpf VARCHAR (14) NOT NULL,
                dt_cadastro DATE DEFAULT (CURDATE()),
                dt_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                CONSTRAINT tbl_cli_id_cli_pk PRIMARY KEY (id_cliente),
                CONSTRAINT tbl_cli_cpf_un UNIQUE (cpf),
                CONSTRAINT tbl_cli_id_contato_fk FOREIGN KEY (id_contato) REFERENCES tbl_contatos (id_contato),
                CONSTRAINT tbl_cli_id_endereco_fk FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos (id_endereco),
            """,
            "csv_file": "tbl_clientes.csv",
            "columns": [
                "id_contato",
                "id_endereco",
                "nome",
                "sobrenome",
                "dt_nascimento",
                "genero",
                "cpf",
            ],
        },
        "tbl_categorias": {
            "schema": """
                id_categoria INTEGER AUTO_INCREMENT,
                categoria VARCHAR (50) NOT NULL,
                CONSTRAINT tbl_categ_id_categ_pk PRIMARY KEY (id_categoria)
            """,
            "csv_file": "tbl_categorias.csv",
            "columns": ["categoria"],
        },
        "tbl_subcategorias": {
            "schema": """
                id_subcategoria INTEGER AUTO_INCREMENT,
                id_categoria INTEGER NOT NULL
                subcategoria VARCHAR (50) NOT NULL,
                CONSTRAINT tbl_subcateg_id_subcateg_pk PRIMARY KEY (id_categoria),
                CONSTRAINT tbl_subcateg_id_categ_fk FOREIGN KEY (id_categoria) REFERENCES tbl_categorias (id_categoria)
            """,
            "csv_file": "tbl_subcategorias.csv",
            "columns": ["id_categoria", "subcategoria"],
        },
        "tbl_produtos": {
            "schema": """
                id_produto INTEGER AUTO_INCREMENT,
                id_marca INTEGER NOT NULL,
                id_categoria INTEGER NOT NULL,
                id_fornecedor INTEGER NOT NULL,
                produto VARCHAR (50) NOT NULL,
                modelo VARCHAR (20) NOT NULL,
                preco_unitario DECIMAL (10, 2) NOT NULL,
                custo_unitario DECIMAL (10, 2) NOT NULL,
                CONSTRAINT tbl_prod_id_prod_pk PRIMARY KEY (id_produto),
                CONSTRAINT tbl_prod_id_marca_fk FOREIGN KEY (id_marca) REFERENCES tbl_marcas (id_marca),
                CONSTRAINT tbl_prod_id_categ_fk FOREIGN KEY (id_categoria) REFERENCES tbl_categorias (id_categoria),
                CONSTRAINT tbl_prod_id_fornec_fk FOREIGN KEY (id_fornecedor) REFERENCES tbl_fornecedores (id_fornecedor),
                CONSTRAINT tbl_prod_preco_unit_ck CHECK (preco_unitario > 0),
                CONSTRAINT tbl_prod_custo_unit_ck CHECK (custo_unitario >= 0)
            """,
            "csv_file": "tbl_produtos.csv",
            "columns": [
                "id_marca",
                "id_categoria",
                "id_fornecedor",
                "produto",
                "modelo",
                "preco_unitario",
                "custo_unitario",
            ],
        },
        "tbl_marcas": {
            "schema": """
                id_marca INTEGER AUTO_INCREMENT,
                marca VARCHAR(50) NOT NULL,
                CONSTRAINT tbl_marcas_id_marca_pk PRIMARY KEY (id_marca)
            """,
            "csv_file": "tbl_marcas.csv",
            "columns": ["marca"],
        },
        "tbl_fornecedores": {
            "schema": """
                id_fornecedor INTEGER AUTO_INCREMENT,
                id_contato INTEGER NOT NULL,
                id_endereco INTEGER NOT NULL,
                fornecedor VARCHAR (50) NOT NULL,
                cnpj VARCHAR (18) NOT NULL,
                CONSTRAINT tbl_fornec_id_fornec_pk PRIMARY KEY (id_fornecedor),
                CONSTRAINT tbl_fornec_id_contato_fk FOREIGN KEY (id_contato) REFERENCES tbl_contatos (id_contato),
                CONSTRAINT tbl_fornec_id_end_fk FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos (id_endereco),
                CONSTRAINT tbl_fornec_cnpj_un UNIQUE (cnpj)
            """,
            "csv_file": "tbl_fornecedores.csv",
            "columns": ["id_contato", "id_endereco", "fornecedor", "cnpj"],
        },
        "tbl_lojas": {
            "schema": """
                id_loja INTEGER AUTO_INCREMENT,
                id_endereco INTEGER NOT NULL,
                loja VARCHAR (50) NOT NULL,
                CONSTRAINT tbl_lojas_id_loja_pk PRIMARY KEY (id_loja),
                CONSTRAINT tbl_lojas_id_endereco_fk FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos (id_endereco)
            """,
            "csv_file": "tbl_lojas.csv",
            "columns": ["id_endereco", "loja"],
        },
        "tbl_status_estoques": {
            "schema": """
                id_status_estoque INTEGER AUTO_INCREMENT,
                reposicao_estoque VARCHAR (20) NOT NULL,
                CONSTRAINT tbl_status_estoques_id_status_estoque_pk PRIMARY KEY (id_status_estoque)
            """,
            "csv_file": "tbl_status_estoques.csv",
            "columns": ["reposicao_estoque"],
        },
        "tbl_estoques": {
            "schema": """
                id_estoque INTEGER AUTO_INCREMENT,
                id_produto INTEGER NOT NULL,
                id_status_estoque INTEGER NOT NULL,
                qtde_disponivel INTEGER NOT NULL,
                dt_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                CONSTRAINT tbl_estoques_id_estoque_pk PRIMARY KEY (id_estoque),
                CONSTRAINT tbl_estoques_id_prod_fk FOREIGN KEY (id_produto) REFERENCES tbl_produtos (id_produto),
                CONSTRAINT tbl_estoques_id_status_estoque_fk FOREIGN KEY (id_status_estoque) REFERENCES tbl_status_estoques (id_status_estoque),
                CONSTRAINT tbl_estoques_qtde_disp_ck CHECK (qtde_disponivel >= 0)
            """,
            "csv_file": "tbl_estoques.csv",
            "columns": ["id_produto", "id_status", "qtde_disponivel"],
        },
        "tbl_departamentos": {
            "schema": """
                id_departamento INTEGER AUTO_INCREMENT,
                departamento VARCHAR (50) NOT NULL,
                CONSTRAINT tbl_depto_id_depto_pk PRIMARY KEY (id_departamento)
            """,
            "csv_file": "tbl_departamentos.csv",
            "columns": ["departamento"],
        },
        "tbl_cargos": {
            "schema": """
                id_cargo INTEGER AUTO_INCREMENT,
                cargo VARCHAR (50) NOT NULL,
                CONSTRAINT tbl_cargos_id_cargo_pk PRIMARY (id_cargo)
            """,
            "csv_file": "tbl_cargos.csv",
            "columns": ["departamento"],
        },
        "tbl_funcionarios": {
            "schema": """
                id_funcionario INTEGER AUTO_INCREMENT,
                id_departamento INTEGER NOT NULL,
                id_cargo INTEGER NOT NULL,
                id_loja INTEGER NOT NULL,
                id_contato INTEGER NOT NULL,
                id_endereco INTEGER NOT NULL,
                nome VARCHAR (50) NOT NULL,
                sobrenome VARCHAR (100) NOT NULL,
                dt_nascimento DATE NOT NULL,
                genero CHAR (1),
                cpf VARCHAR (14) NOT NULL,
                salario DECIMAL (10, 2) NOT NULL,
                dt_admissao DATE NOT NULL,
                dt_demissao DATE,
                CONSTRAINT tbl_func_id_func_pk PRIMARY KEY (id_funcionario),
                CONSTRAINT tbl_func_id_depto_fk FOREIGN KEY (id_departamento) REFERENCES tbl_departamentos (id_departamento),
                CONSTRAINT tbl_func_id_cargo_fk FOREIGN KEY (id_cargo) REFERENCES tbl_cargos (id_cargo),
                CONSTRAINT tbl_func_id_contato_fk FOREIGN KEY (id_contato) REFERENCES tbl_contatos (id_contato),
                CONSTRAINT tbl_func_id_end_fk FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos (id_endereco),
                CONSTRAINT tbl_func_cpf_un UNIQUE (cpf),
                CONSTRAINT tbl_func_salario_ck CHECK (salario > 0),
                CONSTRAINT tbl_func_dt_nascimento_ck CHECK (TIMESTAMPDIFF(YEAR, dt_nascimento, CURDATE()) >= 18)
            """,
            "csv_file": "tbl_funcionarios.csv",
            "columns": [
                "id_departamento",
                "id_cargo",
                "id_contato",
                "id_endereco",
                "nome",
                "sobrenome",
                "dt_nascimento",
                "genero",
                "cpf",
                "salario",
                "dt_admissao",
                "dt_demissao",
            ],
        },
        "tbl_transportadoras": {
            "schema": """
                id_transportadora INTEGER AUTO_INCREMENT,
                id_contato INTEGER NOT NULL,
                id_endereco INTEGER NOT NULL,
                transportadora VARCHAR (50) NOT NULL,
                cnpj VARCHAR (18) NOT NULL,
                CONSTRAINT tbl_transp_id_transp_pk PRIMARY KEY (id_transportadora),
                CONSTRAINT tbl_transp_id_contato_fk FOREIGN KEY (id_contato) REFERENCES tbl_contatos (id_contato),
                CONSTRAINT tbl_transp_id_end_fk FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos (id_endereco),
                CONSTRAINT tbl_transp_cnpj_un UNIQUE (cnpj)
            """,
            "csv_file": "tbl_transportadoras.csv",
            "columns": ["id_contato", "id_endereco", "transportadora", "cnpj"],
        },
        "tbl_pedidos": {
            "schema": """
                id_pedido INTEGER AUTO_INCREMENT,
                id_loja INTEGER NOT NULL,
                id_transportadora INTEGER NOT NULL,
                id_status_pedido INTEGER NOT NULL,
                custo_frete_cliente DECIMAL (10, 2) NOT NULL,
                custo_frete_transportadora DECIMAL (10, 2) NOT NULL,
                dt_pedido DATE NOT NULL,
                dt_estimada_entrega DATE NOT NULL,
                dt_entrega DATE,
                CONSTRAINT tbl_ped_id_ped_pk PRIMARY KEY (id_pedido),
                CONSTRAINT tbl_ped_id_loja_fk FOREIGN KEY (id_loja) REFERENCES tbl_lojas (id_loja),
                CONSTRAINT tbl_ped_id_transp_fk FOREIGN KEY (id_transportadora) REFERENCES tbl_transportadoras (id_transportadora),
                CONSTRAINT tbl_ped_id_status_ped_fk FOREIGN KEY (id_status_pedido) REFERENCES tbl_status_pedidos (id_status_pedido),
                CONSTRAINT tbl_ped_custo_frete_cliente_ck CHECK (custo_frete_cliente >= 0),
                CONSTRAINT tbl_ped_custo_frete_transportadora_ck CHECK (custo_frete_transportadora >= 0)
            """,
            "csv_file": "tbl_pedidos.csv",
            "columns": [
                "id_loja",
                "id_transportadora",
                "id_status_pedido",
                "custo_frete_cliente",
                "custo_frete_transportadora",
                "dt_pedido",
                "dt_estimada_entrega",
                "dt_entrega",
            ],
        },
        "tbl_pagamentos": {
            "schema": """
                id_pagamento INTEGER AUTO_INCREMENT,
                id_pedido INTEGER NOT NULL,
                id_forma_pagamento INTEGER NOT NULL,
                id_status_pagamento INTEGER NOT NULL,
                valor_pago DECIMAL (10, 2) NOT NULL,
                dt_pagamento DATE NOT NULL,
                CONSTRAINT tbl_pgto_id_pgto_pk PRIMARY KEY (id_pagamento),
                CONSTRAINT tbl_pgto_id_ped_fk FOREIGN KEY (id_pedido) REFERENCES tbl_pedidos (id_pedido),
                CONSTRAINT tbl_pgto_id_forma_pgto_fk FOREIGN KEY (id_forma_pagamento) REFERENCES tbl_forma_pagamentos (id_forma_pagamento),
                CONSTRAINT tbl_pgto_id_status_pgto_fk FOREIGN KEY (id_status_pagamento) REFERENCES tbl_status_pagamentos (id_status_pagamento),
                CONSTRAINT tbl_pgto_vl_pago_ck CHECK (valor_pago > 0)
            """,
            "csv_file": "tbl_pagamentos.csv",
            "columns": [
                "id_pedido",
                "id_forma_pagamento",
                "id_status_pagamento",
                "valor_pago",
                "dt_pagamento",
            ],
        },
        "tbl_vendas": {
            "schema": """
                id_venda INTEGER AUTO_INCREMENT,
                id_pedido INTEGER NOT NULL,
                id_cliente INTEGER NOT NULL,
                id_produto INTEGER NOT NULL,
                id_funcionario INTEGER NOT NULL,
                id_canal_venda INTEGER NOT NULL,
                qtde_itens_vendidos INTEGER NOT NULL,
                valor_vendido DECIMAL (10, 2) NOT NULL,
                desconto DECIMAL (2, 2) NOT NULL,
                custo_total DECIMAL  (10, 2) NOT NULL,
                dt_venda DATE NOT NULL,
                CONSTRAINT tbl_vendas_id_venda_pk PRIMARY KEY (id_venda),
                CONSTRAINT tbl_vendas_id_ped_fk FOREIGN KEY (id_pedido) REFERENCES tbl_pedidos (id_pedido),
                CONSTRAINT tbl_vendas_id_cli_fk FOREIGN KEY (id_cliente) REFERENCES tbl_clientes (id_cliente),
                CONSTRAINT tbl_vendas_id_prod_fk FOREIGN KEY (id_produto) REFERENCES tbl_produtos (id_produto),
                CONSTRAINT tbl_vendas_id_func_fk FOREIGN KEY (id_funcionario) REFERENCES tbl_funcionarios (id_funcionario),
                CONSTRAINT tbl_vendas_id_canal_venda_fk FOREIGN KEY (id_canal_venda) REFERENCES tbl_canal_vendas (id_canal_venda),
                CONSTRAINT tbl_vendas_id_pgto_fk FOREIGN KEY (id_pagamento) REFERENCES tbl_pagamentos (id_pagamento),
                CONSTRAINT tbl_vendas_qtde_itens_vendidos_ck CHECK (qtde_itens_vendidos > 0),
                CONSTRAINT tbl_vendas_valor_vendido_ck CHECK (valor_vendido > 0),
                CONSTRAINT tbl_vendas_desconto_ck CHECK (desconto >= 0),
                CONSTRAINT tbl_vendas_custo_total_ck CHECK (valor_pago >= 0)
            """,
            "csv_file": "tbl_vendas.csv",
            "columns": [
                "id_pedido",
                "id_cliente",
                "id_produto",
                "id_funcionario",
                "id_canal_venda",
                "qtde_itens_vendidos",
                "valor_vendido",
                "desconto",
                "custo_total",
                "dt_venda",
            ],
        },
        "tbl_motivo_devolucoes": {
            "schema": """
                id_motivo_devolucao INTEGER AUTO_INCREMENT,
                motivo_devolucao VARCHAR(100),
                CONSTRAINT tbl_motivo_devol_id_motivo_devol_pk PRIMARY KEY (id_motivo_devolucao)
            """,
            "csv_file": "tbl_motivo_devolucoes.csv",
            "columns": ["motivo_devolucao"],
        },
        "tbl_devolucoes": {
            "schema": """
                id_devolucao INTEGER AUTO_INCREMENT,
                id_cliente INTEGER NOT NULL,
                id_pedido INTEGER NOT NULL,
                id_motivo_devolucao INTEGER NOT NULL,
                quantidade INTEGER NOT NULL,
                dt_devolucao DATE NOT NULL,
                CONSTRAINT tbl_devol_id_devol_pk PRIMARY KEY (id_devolucao),
                CONSTRAINT tbl_devol_id_cli_fk_ FOREIGN KEY (id_cliente) REFERENCES tbl_clientes (id_cliente),
                CONSTRAINT tbl_devol_id_ped_fk FOREIGN KEY (id_pedido) REFERENCES tbl_pedidos (id_pedido),
                CONSTRAINT tbl_devol_id_motivo_devol_fk FOREIGN KEY (id_motivo_devolucao) REFERENCES tbl_motivo_devolucoes (id_motivo_devolucao),
                CONSTRAINT tbl_devol_qtde_ck CHECK (quantidade > 0)
            """,
            "csv_file": "tbl_devolucoes.csv",
            "columns": [
                "id_cliente",
                "id_pedido",
                "id_motivo_devolucao",
                "quantidade",
                "dt_devolucao",
            ],
        },
    }

    return dict_tables_config
