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

- Pré-requisitos:

  1. Baixar e instalar o Docker Desktop;

     Link para download: https://www.docker.com/

  2. Baixar e instalar o PgAdmin (Client do PostgreSQL);

     Link para download: https://www.pgadmin.org/download/

  3. Baixar e instalar o Workbench (Client do MySQL);

     Link para download: https://dev.mysql.com/downloads/workbench/

  4. Baixar e instalar o Airbyte;

     Link para download: https://docs.airbyte.com/using-airbyte/getting-started/oss-quickstart

  5. Baixar e instalar o Git;

     Link para download: https://git-scm.com/downloads

<br>

- Passo a passo:

1. Primeira coisa que precisamos fazer é instalar o python. Para isso, vamos utilizar o Pyenv que é um pacote que permite gerenciar diversas versões do Python na mesma máquina.

```
git clone https://github.com/pyenv-win/pyenv-win.git %USERPROFILE%\.pyenv
```

2. Após executar o comando acima, será criada uma pasta no seu usuário chamada .pyenv, que conterá todos os arquivos necessários para que o Pyenv possa funcionar. Agora, precisamos configurar variáveis de ambiente para que o sistema operacional consiga compreender os comandos do Pyenv no prompt de comando. Vá até a lupa de pesquisa e procure por "configurações avançadas do sistema". Em seguida, clique em "Variáveis de ambiente" e posteriormente clique em "Novo" na parte de variáveis do usuário. Após isso, abrirá uma janela para incluir o nome e o valor da variável de ambiente que está logo abaixo.

```
PYENV=C:\Users\seu_usuario\.pyenv\pyenv-win\
PYENV_HOME=C:\Users\seu_usuario\.pyenv\pyenv-win\
PYENV_ROOT=C:\Users\seu_usuario\.pyenv\pyenv-win\
```

3. Para ter certeza que o Pyenv está instalado e funcionando corretamente, abra o prompt de comando e digite:

```
pyenv --version
```

4. Se após a execução do código acima retornar a versão do Pyenv é porque o sistema operacional já está conseguindo compreender os comandos. Caso contrário, revise o passo a passo descrito e se for necessário busque ajuda no Google. Por conseguinte, agora com as configurações necessárias, precisamos instalar o Python através do Pyenv.

```
pyenv install 3.12.1
```

5. Com o Python instalado, precisamos agora clonar o projeto. Caso queira manter o projeto em uma pasta específica, você pode navegar através da estrutura de pastas do seu notebook/computador com o comando "cd nome_pasta". Se não especificar a pasta, provavelmente o projeto será criado na sua pasta de usuário.Feito isso, digite:

```
git clone https://github.com/Kjonnathas/DataWarehouse_MySQL_Airflow.git
```

6. Com o projeto clonado, precisamos especificar a versão do python que irá rodar no projeto. Para isso, execute o seguinte comando dentro da pasta do projeto:

```
pyenv local 3.12.1
```

7. Em seguida, vamos criar nosso ambiente virtual. O ambiente virtual é uma boa prática que visa manter um ambiente único para cada projeto desenvolvido. Sendo assim, execute o comando:

```
python -m venv .venv
```

8. Agora precisamos ativar o ambiente virtual. Para isso, execute:

```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

.venv/Scripts/Activate.ps1
```

9. Depois de ter feito o passo anterior, é preciso agora realizar a instalação das bibliotecas que são utilizadas no projeto. Portanto, dentro da pasta "DataWarehouse_MySQL_Airflow", use o seguinte comando:

```
pip install -r requirements.txt
```

10. Nesse momento, podemos começar a criação do contéiner que rodará o servidor do nosso banco de dados transacional via Docker. Abra o Docker Desktop. Em seguida, abra o prompt de comando caso ainda não esteja aberto ou tenha fechado e execute:

```
docker pull mysql:8.0-debian
```

11. O passo acima fará o download da imagem do MySQL do Docker Hub. Agora, com o download feito, podemos criar o contéiner. Depois de executar o comando abaixo, abra o Docker Desktop e veja se o contéiner foi criado.

```
docker run --name mysql_prod -p 3307:3306 -e MYSQL_ROOT_PASSWORD=escolha_uma_senha -d mysql:8.0-debian
```

12. Vamos aproveitar e criar logo também o servidor que usaremos para armazenar a nossa staging area. Após executar, faça o mesmo check no Docker Desktop para averiguar se o contéiner foi criado direitinho.

```
docker run --name postgres_stg --network bridge -p 5433:5432 -e POSTGRES_DB=escolha_nome_do_banco -e POSTGRES_USER=escolha_nome_do_usuario -e POSTGRES_PASSWORD=escolha_uma_senha -d postgres
```

13. Com o servidor do banco de dados transacional e da staging area criada, podemos avançar na criação das tabelas no banco de dados transacional. Porém, antes de criar as tabelas, precisamos configurar o servidor. Para isso, abra o Workbench (Client do MySQL). Após abrir, clique no botão de "+" ao lado de "MySQL Connections". Com isso, abrirá uma janela para inserir as configurações. Insira um nome para a conexão (da sua escolha), o host - para descobrir o host você pode executar o seguinte comando no prompt de comando "docker inspect mysql_prod". Irá abrir uma estrutura de json e vá até o final e procure por "IPAddress". O valor desse campo é o host da máquina -, a porta (3307) e a senha. Depois disso teste a conexão e veja se deu certo. Se der certo, basta clicar sobre a conexão que irá direcioná-lo para a tela principal do client.

14. Depois de ter feito o passo anterior, vá até o arquivo "database_transacional.sql" que está dentro da pasta "models" que está dentro da pasta "src" e copie todo o conteúdo. Copiado o conteúdo, volte ao Workbench e cole. Depois selecione todo o conteúdo colado e execute (CTRL + Enter ou clique no botão de run). Em seguida, faça um refresh e veja se o banco de dados e as tabelas foram criadas normalmente.

15. Agora que temos o banco de dados e as tabelas criadas, vamos precisar executar um script Python para popular as tabelas que estarão simulando nosso ambiente transacional. Procure pelo script "job_etl.py" dentro da pasta "jobs" que está dentro da pasta "src". Navegue até esta pasta através do seu terminal. Você pode fazer isso usando o seguinte comando:

```
cd src/jobs
```

16. Antes de executarmos o script Python, precisamos criar um arquivo ".env" para armazenar algumas variáveis de ambiente. Sem elas, o script resultará em erro. Portanto, crie este arquivo dentro da pasta "DataWarehouse_MySQL_Airflow" e insira as seguintes informações:

    - MYSQL_USER=root
    - MYSQL_PASSWORD=sua_senha
    - MYSQL_DB=seu_banco_de_dados
    - MYSQL_HOST=seu_host
    - MYSQL_PORT=3307
    - FOLDER_PATH=insira_o_caminho_completo_da_pasta_data
    - FOLDER_LOGS=insira_o_caminho_completo_da_pasta_logs

17. Depois de ter entrado na pasta jobs e configurado o arquivo ".env", basta apenas executar o código Python para que ele possa ler os arquivos csv e depois carregá-los no banco de dados. Para isso, digite no seu terminal:

```
python job_etl.py
```

18. Se o passo anterior deu certo, podemos avançar na criação do contéiner do Airbyte e suas configurações.

# 10. Licença

Este projeto está licenciado sob os termos da licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
