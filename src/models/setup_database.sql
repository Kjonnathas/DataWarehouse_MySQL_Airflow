
-- ##### SEQUÊNCIA DE SCRIPTS SQL PARA CRIAÇÃO DO BANCO DE DADOS TRANSACIONAL (OLTP) #####

-- Criando o banco de dados

CREATE DATABASE IF NOT EXISTS db_prod;

-- Ativando o banco de dados criado

USE db_prod;

-- Criando a tabela de Canal de Vendas

CREATE TABLE IF NOT EXISTS tbl_canal_vendas (
    id_canal_venda INTEGER AUTO_INCREMENT,
    canal_venda VARCHAR (15) NOT NULL,
    CONSTRAINT tbl_canal_vendas_id_canal_venda_pk PRIMARY KEY (id_canal_venda)
);

-- Criando a tabela de Status Pagamento

CREATE TABLE IF NOT EXISTS tbl_status_pagamentos (
    id_status_pagamento INTEGER AUTO_INCREMENT,
    status_pagamento VARCHAR (20) NOT NULL,
    CONSTRAINT tbl_status_pgto_id_status_pgto_pk PRIMARY KEY (id_status_pagamento)
);

-- Criando a tabela de Forma de Pagamento

CREATE TABLE IF NOT EXISTS tbl_forma_pagamentos (
    id_forma_pagamento INTEGER AUTO_INCREMENT,
    tipo_forma_pagamento VARCHAR (20) NOT NULL,
    CONSTRAINT tbl_forma_pgto_id_forma_pgto_pk PRIMARY KEY (id_forma_pagamento)
);

-- Criando a tabela de Status Pedido

CREATE TABLE IF NOT EXISTS tbl_status_pedidos (
    id_status_pedido INTEGER AUTO_INCREMENT,
    status_pedido VARCHAR (50) NOT NULL,
    CONSTRAINT tbl_status_ped_id_status_ped_pk PRIMARY KEY (id_status_pedido)
);

-- Criando a tabela de Referências

CREATE TABLE IF NOT EXISTS tbl_referencias (
    id_referencia INTEGER AUTO_INCREMENT,
    tipo_referencia VARCHAR (20) NOT NULL,
    CONSTRAINT tbl_ref_id_ref_pk PRIMARY KEY (id_referencia)
);

-- Criando a tabela de Países

CREATE TABLE IF NOT EXISTS tbl_paises (
    id_pais INTEGER AUTO_INCREMENT,
    pais VARCHAR (50) NOT NULL,
    CONSTRAINT tbl_paises_id_pais_pk PRIMARY KEY (id_pais)
);

-- Criando a tabela de Estados

CREATE TABLE IF NOT EXISTS tbl_estados (
    id_estado INTEGER AUTO_INCREMENT,
    id_pais INTEGER NOT NULL,
    estado VARCHAR (50) NOT NULL,
    sigla_estado CHAR (2) NOT NULL,
    CONSTRAINT tbl_estados_id_estado_pk PRIMARY KEY (id_estado),
    CONSTRAINT tbl_estados_id_pais_fk FOREIGN KEY (id_pais) REFERENCES tbl_paises (id_pais)
);

-- Criando a tabela de Cidades

CREATE TABLE IF NOT EXISTS tbl_cidades (
    id_cidade INTEGER AUTO_INCREMENT,
    id_estado INTEGER NOT NULL,
    cidade VARCHAR (50) NOT NULL,
    CONSTRAINT tbl_cidades_id_cidade_pk PRIMARY KEY (id_cidade),
    CONSTRAINT tbl_cidades_id_estado_fk FOREIGN KEY (id_estado) REFERENCES tbl_estados (id_estado)
);

-- Criando a tabela de Bairros

CREATE TABLE IF NOT EXISTS tbl_bairros (
    id_bairro INTEGER AUTO_INCREMENT,
    id_cidade INTEGER NOT NULL,
    bairro VARCHAR (100) NOT NULL,
    CONSTRAINT tbl_cidades_id_bairro_pk PRIMARY KEY (id_bairro),
    CONSTRAINT tbl_cidades_id_cidade_fk FOREIGN KEY (id_cidade) REFERENCES tbl_cidades (id_cidade)
);

-- Criando a tabela de Endereços

CREATE TABLE IF NOT EXISTS tbl_enderecos (
    id_endereco INTEGER AUTO_INCREMENT,
    id_referencia INTEGER NOT NULL,
    id_bairro INTEGER NOT NULL,
    logradouro VARCHAR (100) NOT NULL,
    numero INTEGER NOT NULL,
    cep VARCHAR (20) NOT NULL,
    CONSTRAINT tbl_end_id_end_pk PRIMARY KEY (id_endereco),
    CONSTRAINT tbl_end_id_ref_fk FOREIGN KEY (id_referencia) REFERENCES tbl_referencias (id_referencia),
    CONSTRAINT tbl_end_id_bairro_fk FOREIGN KEY (id_bairro) REFERENCES tbl_bairros (id_bairro)
);

-- Criando a tabela de Tipo de Contatos

CREATE TABLE IF NOT EXISTS tbl_tipos_contatos (
    id_tipo_contato INTEGER AUTO_INCREMENT,
    tipo_contato VARCHAR (30) NOT NULL,
    CONSTRAINT tbl_tipos_contatos_id_tipo_contato_pk PRIMARY KEY (id_tipo_contato)
);

-- Criando a tabela de Contatos

CREATE TABLE IF NOT EXISTS tbl_contatos (
    id_contato INTEGER AUTO_INCREMENT,
    id_tipo_contato INTEGER NOT NULL,
    id_referencia INTEGER NOT NULL,
    telefone VARCHAR (13) NOT NULL,
    email VARCHAR (50) NOT NULL,
    status_contato CHAR (1) NOT NULL,
    CONSTRAINT tbl_contatos_id_contato_pk PRIMARY KEY (id_contato),
    CONSTRAINT tbl_contatos_id_tipo_contato_fk FOREIGN KEY (id_tipo_contato) REFERENCES tbl_tipo_contatos (id_tipo_contato),
    CONSTRAINT tbl_contatos_id_ref_fk FOREIGN KEY (id_referencia) REFERENCES tbl_referencias (id_referencia),
    CONSTRAINT tbl_contatos_telefone_ck CHECK (id_tipo_contato IN (1, 2, 3) AND telefone NOT LIKE '%@%' OR id_tipo_contato NOT IN (1, 2, 3)),
    CONSTRAINT tbl_contatos_email_ck CHECK (id_tipo_contato = 4 AND email LIKE '%@%' OR id_tipo_contato != 4)
);

-- Criando a tabela de Clientes

CREATE TABLE IF NOT EXISTS tbl_clientes (
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
    CONSTRAINT tbl_cli_id_endereco_fk FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos (id_endereco)
);

-- Criando a tabela de Categorias

CREATE TABLE IF NOT EXISTS tbl_categorias (
    id_categoria INTEGER AUTO_INCREMENT,
    categoria VARCHAR (50) NOT NULL,
    CONSTRAINT tbl_categ_id_categ_pk PRIMARY KEY (id_categoria)
);

-- Criando a tabela de Subcategorias

CREATE TABLE IF NOT EXISTS tbl_subcategorias (
    id_subcategoria INTEGER AUTO_INCREMENT,
    id_categoria INTEGER NOT NULL
    subcategoria VARCHAR (50) NOT NULL,
    CONSTRAINT tbl_subcateg_id_subcateg_pk PRIMARY KEY (id_subcategoria),
    CONSTRAINT tbl_subcateg_id_categ_fk FOREIGN KEY (id_categoria) REFERENCES tbl_categorias (id_categoria)
)

-- Criando a tabela de Marcas

CREATE TABLE IF NOT EXISTS tbl_marcas (
    id_marca INTEGER AUTO_INCREMENT,
    marca VARCHAR(50) NOT NULL,
    CONSTRAINT tbl_marcas_id_marca_pk PRIMARY KEY (id_marca)
);

-- Criando a tabela de Fornecedores

CREATE TABLE IF NOT EXISTS tbl_fornecedores (
    id_fornecedor INTEGER AUTO_INCREMENT,
    id_contato INTEGER NOT NULL,
    id_endereco INTEGER NOT NULL,
    fornecedor VARCHAR (50) NOT NULL,
    cnpj VARCHAR (18) NOT NULL,
    CONSTRAINT tbl_fornec_id_fornec_pk PRIMARY KEY (id_fornecedor),
    CONSTRAINT tbl_fornec_id_contato_fk FOREIGN KEY (id_contato) REFERENCES tbl_contatos (id_contato),
    CONSTRAINT tbl_fornec_id_end_fk FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos (id_endereco),
    CONSTRAINT tbl_fornec_cnpj_un UNIQUE (cnpj)
);

-- Criando a tabela de Produtos

CREATE TABLE IF NOT EXISTS tbl_produtos (
    id_produto INTEGER AUTO_INCREMENT,
    id_marca INTEGER NOT NULL,
    id_categoria INTEGER NOT NULL,
    id_fornecedor INTEGER NOT NULL,
    produto VARCHAR (100) NOT NULL,
    modelo VARCHAR (100) NOT NULL,
    preco_unitario DECIMAL (10, 2) NOT NULL,
    custo_unitario DECIMAL (10, 2) NOT NULL,
    CONSTRAINT tbl_prod_id_prod_pk PRIMARY KEY (id_produto),
    CONSTRAINT tbl_prod_id_marca_fk FOREIGN KEY (id_marca) REFERENCES tbl_marcas (id_marca),
    CONSTRAINT tbl_prod_id_categ_fk FOREIGN KEY (id_categoria) REFERENCES tbl_categorias (id_categoria),
    CONSTRAINT tbl_prod_id_fornec_fk FOREIGN KEY (id_fornecedor) REFERENCES tbl_fornecedores (id_fornecedor),
    CONSTRAINT tbl_prod_preco_unit_ck CHECK (preco_unitario > 0),
    CONSTRAINT tbl_prod_custo_unit_ck CHECK (custo_unitario >= 0)
);

-- Criando a tabela de Lojas

CREATE TABLE IF NOT EXISTS tbl_lojas (
    id_loja INTEGER AUTO_INCREMENT,
    id_endereco INTEGER NOT NULL,
    loja VARCHAR (50) NOT NULL,
    CONSTRAINT tbl_lojas_id_loja_pk PRIMARY KEY (id_loja),
    CONSTRAINT tbl_lojas_id_endereco_fk FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos (id_endereco)
);

-- Criando a tabela de Status de Estoque

CREATE TABLE IF NOT EXISTS tbl_status_estoques (
    id_status_estoque INTEGER AUTO_INCREMENT,
    reposicao_estoque VARCHAR (20) NOT NULL,
    CONSTRAINT tbl_status_estoques_id_status_estoque_pk PRIMARY KEY (id_status_estoque)
);

-- Criando a tabela de Estoques

CREATE TABLE IF NOT EXISTS tbl_estoques (
    id_estoque INTEGER AUTO_INCREMENT,
    id_produto INTEGER NOT NULL,
    id_status_estoque INTEGER NOT NULL,
    qtde_disponivel INTEGER NOT NULL,
    dt_atualizacao DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT tbl_estoques_id_estoque_pk PRIMARY KEY (id_estoque),
    CONSTRAINT tbl_estoques_id_prod_fk FOREIGN KEY (id_produto) REFERENCES tbl_produtos (id_produto),
    CONSTRAINT tbl_estoques_id_status_estoque_fk FOREIGN KEY (id_status_estoque) REFERENCES tbl_status_estoques (id_status_estoque),
    CONSTRAINT tbl_estoques_qtde_disp_ck CHECK (qtde_disponivel >= 0)
);

-- Criando a tabela de Departamentos

CREATE TABLE IF NOT EXISTS tbl_departamentos (
    id_departamento INTEGER AUTO_INCREMENT,
    departamento VARCHAR (50) NOT NULL,
    CONSTRAINT tbl_depto_id_depto_pk PRIMARY KEY (id_departamento)
);

-- Criando a tabela de Cargos

CREATE TABLE IF NOT EXISTS tbl_cargos (
    id_cargo INTEGER AUTO_INCREMENT,
    cargo VARCHAR (50) NOT NULL,
    CONSTRAINT tbl_cargos_id_cargo_pk PRIMARY (id_cargo)
);

-- Criando a tabela de Funcionários

CREATE TABLE IF NOT EXISTS tbl_funcionarios (
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
    CONSTRAINT tbl_func_salario_ck CHECK (salario > 0)
);

-- Criando a tabela de Transportadoras

CREATE TABLE IF NOT EXISTS tbl_transportadoras (
    id_transportadora INTEGER AUTO_INCREMENT,
    id_contato INTEGER NOT NULL,
    id_endereco INTEGER NOT NULL,
    transportadora VARCHAR (50) NOT NULL,
    cnpj VARCHAR (18) NOT NULL,
    CONSTRAINT tbl_transp_id_transp_pk PRIMARY KEY (id_transportadora),
    CONSTRAINT tbl_transp_id_contato_fk FOREIGN KEY (id_contato) REFERENCES tbl_contatos (id_contato),
    CONSTRAINT tbl_transp_id_end_fk FOREIGN KEY (id_endereco) REFERENCES tbl_enderecos (id_endereco),
    CONSTRAINT tbl_transp_cnpj_un UNIQUE (cnpj)
);

-- Criando a tabela de Pedidos

CREATE TABLE IF NOT EXISTS tbl_pedidos (
    id_pedido INTEGER AUTO_INCREMENT,
    id_loja INTEGER NOT NULL,
    id_transportadora INTEGER NOT NULL,
    id_status_pedido INTEGER NOT NULL,
    dt_pedido DATE NOT NULL,
    dt_estimada_entrega DATE NOT NULL,
    dt_entrega DATE,
    custo_frete_transportadora DECIMAL (10, 2) NOT NULL,
    custo_frete_cliente DECIMAL (10, 2) NOT NULL,
    CONSTRAINT tbl_ped_id_ped_pk PRIMARY KEY (id_pedido),
    CONSTRAINT tbl_ped_id_loja_fk FOREIGN KEY (id_loja) REFERENCES tbl_lojas (id_loja),
    CONSTRAINT tbl_ped_id_transp_fk FOREIGN KEY (id_transportadora) REFERENCES tbl_transportadoras (id_transportadora),
    CONSTRAINT tbl_ped_id_status_ped_fk FOREIGN KEY (id_status_pedido) REFERENCES tbl_status_pedidos (id_status_pedido),
    CONSTRAINT tbl_ped_custo_frete_cliente_ck CHECK (custo_frete_cliente >= 0),
    CONSTRAINT tbl_ped_custo_frete_transportadora_ck CHECK (custo_frete_transportadora >= 0)
);

-- Criando a tabela de Pagamentos

CREATE TABLE IF NOT EXISTS tbl_pagamentos (
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
);

-- Criando a tabela de Vendas

CREATE TABLE IF NOT EXISTS tbl_vendas (
    id_venda INTEGER AUTO_INCREMENT,
    id_pedido INTEGER NOT NULL,
    id_cliente INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    id_funcionario INTEGER NOT NULL,
    id_canal_venda INTEGER NOT NULL,
    qtde_itens_vendidos INTEGER NOT NULL,
    desconto DECIMAL (2, 2) NOT NULL,
    dt_venda DATE NOT NULL,
    valor_vendido DECIMAL (10, 2) NOT NULL,
    custo_total DECIMAL  (10, 2) NOT NULL,
    CONSTRAINT tbl_vendas_id_venda_pk PRIMARY KEY (id_venda),
    CONSTRAINT tbl_vendas_id_ped_fk FOREIGN KEY (id_pedido) REFERENCES tbl_pedidos (id_pedido),
    CONSTRAINT tbl_vendas_id_cli_fk FOREIGN KEY (id_cliente) REFERENCES tbl_clientes (id_cliente),
    CONSTRAINT tbl_vendas_id_prod_fk FOREIGN KEY (id_produto) REFERENCES tbl_produtos (id_produto),
    CONSTRAINT tbl_vendas_id_func_fk FOREIGN KEY (id_funcionario) REFERENCES tbl_funcionarios (id_funcionario),
    CONSTRAINT tbl_vendas_id_canal_venda_fk FOREIGN KEY (id_canal_venda) REFERENCES tbl_canal_vendas (id_canal_venda),
    CONSTRAINT tbl_vendas_qtde_itens_vendidos_ck CHECK (qtde_itens_vendidos > 0),
    CONSTRAINT tbl_vendas_valor_vendido_ck CHECK (valor_vendido > 0),
    CONSTRAINT tbl_vendas_desconto_ck CHECK (desconto >= 0),
    CONSTRAINT tbl_vendas_custo_total_ck CHECK (custo_total >= 0)
);

-- Criando a tabela de Motivos de Devoluções

CREATE TABLE tbl_motivo_devolucoes (
    id_motivo_devolucao INTEGER AUTO_INCREMENT,
    motivo_devolucao VARCHAR(100),
    CONSTRAINT tbl_motivo_devol_id_motivo_devol_pk PRIMARY KEY (id_motivo_devolucao)
);

-- Criando a tabela de Devoluções

CREATE TABLE tbl_devolucoes (
    id_devolucao INTEGER AUTO_INCREMENT,
    id_cliente INTEGER NOT NULL,
    id_pedido INTEGER NOT NULL,
    id_motivo_devolucao INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    dt_devolucao DATE NOT NULL,
    CONSTRAINT tbl_devol_id_devol_pk PRIMARY KEY (id_devolucao),
    CONSTRAINT tbl_devol_id_cli_fk FOREIGN KEY (id_cliente) REFERENCES tbl_clientes (id_cliente),
    CONSTRAINT tbl_devol_id_ped_fk FOREIGN KEY (id_pedido) REFERENCES tbl_pedidos (id_pedido),
    CONSTRAINT tbl_devol_id_motivo_devol_fk FOREIGN KEY (id_motivo_devolucao) REFERENCES tbl_motivo_devolucoes (id_motivo_devolucao),
    CONSTRAINT tbl_devol_qtde_ck CHECK (quantidade > 0)
);
