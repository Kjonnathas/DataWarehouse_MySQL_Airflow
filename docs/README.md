![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

# 1. Descrição do Projeto

Este projeto foi desenvolvido com o objetivo de criar uma estrutura robusta de Data Warehouse, abrangendo desde a implementação da modelagem conceitual, lógica e física. O trabalho incluiu a criação de um banco de dados transacional (OLTP) e a implementação de um pipeline ETL (Extração, Transformação e Carregamento) para integrar os dados ao Data Warehouse (DW).

O fluxo de dados foi estruturado da seguinte forma:

1. Banco de Dados Transacional (OLTP): Armazenamento inicial dos dados em uma estrutura otimizada para transações.

2. Staging Area: Um ambiente intermediário para a integração e pré-processamento dos dados extraídos.

3. Data Warehouse: Repositório final onde os dados transformados são organizados para análises.

Este projeto demonstra o processo completo de desenvolvimento de um Data Warehouse, desde a modelagem inicial até a automação de pipelines ETL, proporcionando uma base sólida para análises de dados e suporte à tomada de decisões.

# 2. Objetivo do Projeto

Desenvolver uma solução completa de Data Warehouse que integre modelagem de dados, criação de um banco transacional (OLTP) e automação de pipelines ETL, utilizando tecnologias modernas como Docker, Airbyte e Apache Airflow. O projeto visa demonstrar, na prática, o fluxo completo de dados desde a origem até a consolidação em um ambiente otimizado para análises estratégicas, com foco em escalabilidade, portabilidade e organização eficiente dos dados. Além disso, busca aplicar os conhecimentos adquiridos na formação de Engenheiro de Dados da Data Science Academy, servindo como inspiração para que outros profissionais possam utilizar esta arquitetura em seus próprios projetos, tanto pessoais quanto profissionais.

# 3. Arquitetura do Projeto

![Arquitetura do Projeto Data Warehouse](/assets/images/arquitetura_projeto.png)

# 4. Modelagem de Dados

## 4.1 Modelo Conceitual (Diagrama Entidade-Relacionamento - DER)

![Modelo Conceitual](/assets/images/modelo_conceitual.png)

## 4.2 Modelo Lógico

![Modelo Lógico](/assets/images/modelo_logico.png)

## 4.3 Modelo Dimensional

![Modelo Dimensional](/assets/images/modelo_dimensional.png)

# 5. Tecnologias Utilizadas

- Git
- SQL
- PostgreSQL
- MySQL
- Python
- Airbyte
- Apache Airflow
- Docker
- UML

# 6. Descrição de como as Tecnologias foram utilizadas através da ótica da Arquitetura

1.  Criação do Banco de Dados Transacional (OLTP) 🏦

    - Foram gerados diversos arquivos CSV contendo os dados de entrada.
    - Um script Python foi desenvolvido para realizar o carregamento automático desses arquivos no MySQL, configurado como o banco de dados transacional (OLTP).
    - O banco OLTP foi implementado em um servidor dedicado, executado dentro de um contêiner Docker, e consistia em cerca de 30 tabelas criadas previamente através de scripts SQL executados diretamente no cliente do MySQL.

2.  Staging Area 🛠️

    - Para a staging area, foi configurado outro servidor com PostgreSQL, também rodando em um contêiner Docker independente.
    - A ferramenta Airbyte foi utilizada para estabelecer a conexão entre o banco OLTP (MySQL) e a staging area (PostgreSQL). Essa etapa foi responsável pela extração e carga inicial dos dados, garantindo a separação lógica entre os ambientes.

3.  Transformação e Carga no Data Warehouse (DW) 📊

    - O Apache Airflow foi configurado para orquestrar o pipeline de ETL, utilizando uma DAG personalizada que:

      - Extrai os dados da staging area no PostgreSQL.

      - Transforma os dados aplicando as regras de negócio necessárias.
      - Carrega os dados no Data Warehouse, que também foi implementado em PostgreSQL, mas em um servidor e contêiner Docker dedicados.

    - As tabelas do DW foram previamente criadas através de scripts SQL no cliente do PostgreSQL, garantindo que a estrutura estivesse alinhada ao modelo de dados definido para o projeto.

4.  Automatização e Integração 🔄

    - Todo o processo de ETL foi automatizado, permitindo a execução contínua e eficiente do fluxo de dados entre os diferentes ambientes.

Este projeto não apenas simula uma arquitetura real de Data Warehouse como também aplica conceitos fundamentais de engenharia de dados e automação de pipelines. 🐍🐘⚙️

# 7. Descrição de como as Tecnologias foram utilizadas através da ótica das Ferramentas

1. <strong> 🐍 Python </strong>

   O Python foi utilizado para desenvolver scripts que automatizam o carregamento dos dados no MySQL, que funcionou como banco de dados transacional (OLTP) com cerca de 30 tabelas. Os arquivos CSV gerados foram processados e carregados via scripts Python, que atuaram como a ponte entre os dados e o banco de dados, garantindo que as informações fossem corretamente inseridas nas tabelas do MySQL. Além disso, o Python também foi utilizado para criar a DAG (Directed Acyclic Graph) no Apache Airflow, orquestrando o fluxo de trabalho do processo de ETL.

2. <strong> 🐳 Docker Desktop </strong>

   O Docker Desktop foi utilizado para criar contêineres isolados e garantir que cada serviço funcionasse em um ambiente controlado e separado. Criei um contêiner com o MySQL, que foi responsável pelo banco de dados transacional (OLTP), e um contêiner separado com o PostgreSQL para simular a staging area. Além disso, o PostgreSQL foi utilizado no Data Warehouse (DW), que também foi configurado dentro de um contêiner Docker em um servidor separado. O uso de contêineres facilitou a gestão dos serviços e a escalabilidade do projeto.

3. <strong> 🪼 Airbyte </strong>

   O Airbyte foi utilizado como ferramenta de integração de dados, conectando a fonte de dados (MySQL) à staging area (PostgreSQL). Ele foi responsável por extrair os dados do banco de dados MySQL e transferi-los para o PostgreSQL, garantindo que os dados estivessem prontos para serem processados e transformados no fluxo de ETL. O Airbyte automatizou esse processo de movimentação de dados, garantindo a consistência e a atualização das informações.

4. <strong> ☁️ Apache Airflow </strong>

   O Apache Airflow foi a plataforma escolhida para orquestrar todo o processo de ETL. Criei uma DAG (Directed Acyclic Graph) no Airflow para automatizar o fluxo de trabalho. A DAG buscava os dados da staging area no PostgreSQL, aplicava as transformações necessárias e, em seguida, carregava os dados transformados no Data Warehouse (DW), que também estava hospedado no PostgreSQL. O Airflow garantiu que as etapas do processo de transformação e carregamento dos dados fossem executadas de forma sequencial e programada.

5. <strong> 🐬 MySQL </strong>

   O MySQL foi utilizado como o banco de dados transacional (OLTP) responsável pelo armazenamento das tabelas operacionais com cerca de 30 tabelas. O MySQL recebeu os dados de entrada, que foram carregados por meio de scripts Python. Esse banco de dados foi fundamental para o armazenamento e gerenciamento dos dados brutos, que depois seriam processados e transformados para análises posteriores.

6. <strong> 🐘 PostgreSQL </strong>

   O PostgreSQL foi utilizado de duas maneiras: como a staging area e como o banco de dados do Data Warehouse (DW). Na staging area, o PostgreSQL recebeu os dados extraídos do MySQL via Airbyte, e no Data Warehouse, o PostgreSQL foi utilizado para armazenar os dados transformados, permitindo consultas analíticas e a geração de insights de forma eficiente. Antes do processo de ETL começar, as tabelas foram criadas no PostgreSQL com scripts SQL, que definiram a estrutura do banco de dados.

# 8. Exibição do Projeto

## 8.1 Contêineres Docker

![Cônteires Docker](/assets/images/docker.png)

## 8.2 Banco de Dados Transacional no MySQL

### 8.2.1 Tabelas do Banco de Dados

![Banco de Dados MySQL](/assets/images/mysql_1.png)

### 8.2.2 Tabela de Produtos

![Tabela de Produtos no MySQL](/assets/images/mysql_2.png)

### 8.2.3 Tabela de Pedidos

![Tabela de Pedidos no MySQL](/assets/images/mysql_3.png)

### 8.2.4 Tabela de Endereços

![Tabela de Endereços no MySQL](/assets/images/mysql_4.png)

## 8.3 Airbyte

### 8.3.1 Airbyte Source (Fonte de Dados)

![Source do Airbyte](/assets/images/airbyte_1.png)

### 8.3.2 Airbyte Destination (Destino dos Dados)

![Destination do Airbyte](/assets/images/airbyte_2.png)

### 8.3.3 Airbyte Connections (Conexão dos Dados)

![Connection do Airbyte](/assets/images/airbyte_3.png)

![Connection do Airbyte](/assets/images/airbyte_4.png)

## 8.4 Área Intermediária e Banco de Dados Analítico no PostgreSQL

### 8.4.1 Servidores PostgreSQL

![Servidores PostgreSQL](/assets/images/postgresql_1.png)

### 8.4.2 Servidor da Staging Area

![Servidor da Staging Area](/assets/images/postgresql_2.png)

### 8.4.3 Tabelas no Schema da Staging Area

![Tabelas no Schema da Staging Area](/assets/images/postgresql_3.png)

### 8.4.4 Servidor do Data Warehouse (DW)

![Servidor do Data Warehouse](/assets/images/postgresql_4.png)

### 8.4.5 Tabelas no Schema do Data Warehouse

![Tabelas no Schema do Data Warehouse](/assets/images/postgresql_5.png)

### 8.4.6 Tabela Fato Vendas

![Tabela Fato Vendas](/assets/images/postgresql_6.png)

### 8.4.7 Tabela Dimensão Cliente

![Tabela Dimensão Cliente](/assets/images/postgresql_7.png)

## 8.5 Airflow

### 8.5.1 Área de DAGS

![Área de DAGS no Airflow](/assets/images/airflow_1.png)

### 8.5.2 Fluxo da DAG

![Fluxo da DAG no Airflow](/assets/images/airflow_2.png)

![Fluxo da DAG no Airflow](/assets/images/airflow_3.png)

![Fluxo da DAG no Airflow](/assets/images/airflow_4.png)

![Fluxo da DAG no Airflow](/assets/images/airflow_5.png)

![Fluxo da DAG no Airflow](/assets/images/airflow_6.png)

# 9. Instalação e Configuração (Replicação)

# 10. Licença
