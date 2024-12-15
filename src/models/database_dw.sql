
-- ##### SEQUÊNCIA DE SCRIPTS SQL PARA CRIAÇÃO DO BANCO DE DADOS ANALÍTICO (OLAP) #####

-- Criando o banco de dados

CREATE DATABASE IF NOT EXISTS db_dw;

-- Criando o Schema

CREATE SCHEMA IF NOT EXISTS schema_dw;

-- Criando a Dimensão Produto

CREATE TABLE IF NOT EXISTS schema_dw.dim_produto (
    sk_produto INT GENERATED ALWAYS AS IDENTITY,
    nk_produto INT NOT NULL,
    produto VARCHAR (100) NOT NULL,
    modelo VARCHAR (100) NOT NULL,
    marca VARCHAR (50) NOT NULL,
    categoria VARCHAR (50) NOT NULL,
    subcategoria VARCHAR (50) NOT NULL,
    CONSTRAINT dim_prod_sk_produto_pk PRIMARY KEY (sk_produto)
);

-- Criando a Dimensão Localidade

CREATE TABLE IF NOT EXISTS schema_dw.dim_localidade (
    sk_localidade INT GENERATED ALWAYS AS IDENTITY,
    nk_localidade INT NOT NULL,
    logradouro VARCHAR (100) NOT NULL,
    numero INT NOT NULL,
    bairro VARCHAR (100) NOT NULL,
    cidade VARCHAR (50) NOT NULL,
    estado VARCHAR (50) NOT NULL,
    sigla_estado VARCHAR (2) NOT NULL,
    pais VARCHAR (50) NOT NULL,
    cep VARCHAR (20) NOT NULL,
    CONSTRAINT dim_loc_sk_loc_pk PRIMARY KEY (sk_localidade)
);

-- Criando a Dimensão Cliente

CREATE TABLE IF NOT EXISTS schema_dw.dim_cliente (
    sk_cliente INT GENERATED ALWAYS AS IDENTITY,
    nk_cliente INT NOT NULL,
    nome_completo VARCHAR (100) NOT NULL,
    dt_nascimento DATE NOT NULL,
    idade INT NOT NULL,
    genero CHAR (1) NOT NULL,
    CONSTRAINT dim_cli_sk_cli_pk PRIMARY KEY (sk_cliente)
);

-- Criando a Dimensão Vendedor

CREATE TABLE IF NOT EXISTS schema_dw.dim_vendedor (
    sk_vendedor INT GENERATED ALWAYS AS IDENTITY,
    nk_vendedor INT NOT NULL,
    nome_completo VARCHAR (100) NOT NULL,
    dt_nascimento DATE NOT NULL,
    idade INT NOT NULL,
    genero CHAR (1) NOT NULL,
    dt_contratacao DATE NOT NULL,
    CONSTRAINT dim_vendedor_sk_vendedor_pk PRIMARY KEY (sk_vendedor)
);

-- Criando a Dimensão Loja

CREATE TABLE IF NOT EXISTS schema_dw.dim_loja (
    sk_loja INT GENERATED ALWAYS AS IDENTITY,
    nk_loja INT NOT NULL,
    loja VARCHAR (100) NOT NULL,
    CONSTRAINT dim_loja_sk_loja_pk PRIMARY KEY (sk_loja)
);

-- Criando a Dimensão Canal Venda

CREATE TABLE IF NOT EXISTS schema_dw.dim_canal_venda (
    sk_canal_venda INT GENERATED ALWAYS AS IDENTITY,
    nk_canal_venda INT NOT NULL,
    canal_venda VARCHAR (15) NOT NULL,
    CONSTRAINT dim_canal_venda_sk_canal_venda_pk PRIMARY KEY (sk_canal_venda)
);

-- Criando a Dimensão Tempo

CREATE TABLE IF NOT EXISTS schema_dw.dim_tempo (
    sk_tempo INT GENERATED ALWAYS AS IDENTITY,
    data DATE NOT NULL,
    dia INT NOT NULL,
    mes INT NOT NULL,
    mes_por_extenso VARCHAR (9) NOT NULL,
    ano INT NOT NULL,
    ano_abreviado INT NOT NULL,
    dia_da_semana VARCHAR (13),
    semana_do_ano INT NOT NULL,
    trimestre INT NOT NULL,
    semestre INT NOT NULL,
    flag_final_de_semana INT NOT NULL,
    flag_dia_util INT NOT NULL,
    flag_feriado INT NOT NULL,
    CONSTRAINT dim_tempo_sk_tempo_pk PRIMARY KEY (sk_tempo)
);

-- Criando a Fato Vendas

CREATE TABLE IF NOT EXISTS schema_dw.fato_vendas (
    sk_produto INT NOT NULL,
    sk_vendedor INT NOT NULL,
    sk_cliente INT NOT NULL,
    sk_canal_venda INT NOT NULL,
    sk_loja INT NOT NULL,
    sk_localidade INT NOT NULL,
    sk_tempo INT NOT NULL,
    nk_venda INT NOT NULL,
    qtde_itens_vendidos INT NOT NULL,
    valor_vendido DECIMAL (10, 2) NOT NULL,
    custo_total DECIMAL (10, 2) NOT NULL,
    desconto DECIMAL (10, 2) NOT NULL,
    lucro_total DECIMAL (10, 2) NOT NULL,
    CONSTRAINT ft_vendas_pk PRIMARY KEY (sk_produto, sk_vendedor, sk_cliente, sk_canal_venda, sk_loja, sk_localidade, sk_tempo),
    CONSTRAINT ft_vendas_sk_prod_fk FOREIGN KEY (sk_produto) REFERENCES schema_dw.dim_produto (sk_produto),
    CONSTRAINT ft_vendas_sk_vendedor_fk FOREIGN KEY (sk_vendedor) REFERENCES schema_dw.dim_vendedor(sk_vendedor),
    CONSTRAINT ft_vendas_sk_cli_fk FOREIGN KEY (sk_cliente) REFERENCES schema_dw.dim_cliente (sk_cliente),
    CONSTRAINT ft_vendas_sk_canal_venda_fk FOREIGN KEY (sk_canal_venda) REFERENCES schema_dw.dim_canal_venda (sk_canal_venda),
    CONSTRAINT ft_vendas_sk_loja_fk FOREIGN KEY (sk_loja) REFERENCES schema_dw.dim_loja (sk_loja),
    CONSTRAINT ft_vendas_sk_loc_fk FOREIGN KEY (sk_localidade) REFERENCES schema_dw.dim_localidade (sk_localidade),
    CONSTRAINT ft_vendas_sk_tempo_fk FOREIGN KEY (sk_tempo) REFERENCES schema_dw.dim_tempo (sk_tempo)
);