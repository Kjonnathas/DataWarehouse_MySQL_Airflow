from datetime import datetime, timedelta
from time import time
import pendulum
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from contextlib import contextmanager
import logging
from dotenv import load_dotenv
import os
from airflow.models.models_dw import sql_models
from typing import Generator

date = datetime.today()
day = date.day
month = date.month
year = date.year

dotenv_path = "/opt/airflow/config/.env"
load_dotenv(dotenv_path)

logs = os.getenv("FOLDER_LOGS")
if not logs:
    raise EnvironmentError("A variável de ambiente 'FOLDER_LOGS' não foi configurada.")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=os.path.join(logs, f"pipeline_{day}_{month}_{year}.log"),
    filemode="a",
)

default_args = {
    "owner": "data_engineer",
    "email": ["kjonnathas@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": True,
    "retries": 1,
    "retry_delay": timedelta(seconds=30),
}


@contextmanager
def postgres_connection(conn_id) -> Generator[PostgresHook, None, None]:
    """
    Gerencia a conexão PostgreSQL como um contexto.

    Parâmetros:
        conn_id: ID da conexão configurada no Airflow.

    """
    hook = PostgresHook(postgres_conn_id=conn_id)
    conn = hook.get_conn()
    try:
        yield hook
    finally:
        conn.close()


def process_table(
    sql_query: str,
    destination_table: str,
    target_fields: list,
    conn_id: str,
    dw_conn_id: str = "postgres_data_warehouse",
) -> None:
    """
    Processa tabelas, extraindo dados da área de staging e carregando no data warehouse.

    Parâmetros:
        sql_query: Query SQL para buscar dados na área de staging.

        tabela_destino: Nome da tabela de destino no data warehouse.

        target_fields: Lista de colunas para mapear os dados.

        staging_conn_id: Conexão do Airflow com a área de staging.

        dw_conn_id: Conexão do Airflow com o data warehouse.
    """
    logging.info(f"Processando tabela: {destination_table}")
    start = time()

    with postgres_connection(conn_id) as staging_hook:
        try:
            records = staging_hook.get_records(sql=sql_query)
        except Exception as e:
            logging.error(f"Erro ao buscar dados da área de staging: {e}")
            raise

    if not records:
        logging.warning(f"Nenhum dado encontrado para {destination_table}.")
        return None

    with postgres_connection(dw_conn_id) as dw_hook:
        try:
            try:
                dw_hook.run(
                    sql=f"TRUNCATE TABLE {destination_table} RESTART IDENTITY CASCADE"
                )
            except Exception as e:
                logging.error(
                    f"Erro ao truncar os dados na tabela {destination_table}: {e}"
                )
            dw_hook.insert_rows(
                table=destination_table,
                rows=records,
                target_fields=target_fields,
            )
        except Exception as e:
            logging.error(f"Erro ao inserir dados na tabela {destination_table}: {e}")
            raise

    duration = time() - start
    logging.info(
        f"{len(records)} registros processados para {destination_table} em {duration:.2f} segundos."
    )


def process_entity(entity_key: str, entity_type: str = "dimensao") -> None:
    """
    Processa dinamicamente qualquer entidade (dimensão ou fato), com base no modelo de dados.

    Parâmetros:
        entity_key: Chave da entidade nos modelos SQL.
        entity_type: Tipo da entidade ('dimensao' ou 'fato'). Default é 'dimensao'.
    """
    try:
        models = sql_models()
        entity = models.get(entity_key)
        if not entity:
            raise ValueError(f"Chave {entity_key} não encontrada nos modelos.")

        if entity_key == "fato_vendas_temp":
            with postgres_connection("postgres_data_warehouse") as dw_hook:
                logging.info(f"Criando tabela temporária {entity_key}.")
                try:
                    dw_hook.run(
                        sql="""
                            CREATE TABLE IF NOT EXISTS schema_dw.fato_vendas_temp (
                                id_produto INT,
                                id_vendedor INT,
                                id_cliente INT,
                                id_canal_venda INT,
                                id_loja INT,
                                id_localidade INT,
                                dt_venda DATE,
                                nk_venda INT,
                                qtde_itens_vendidos INT,
                                valor_vendido DECIMAL(10, 2),
                                custo_total DECIMAL(10, 2),
                                desconto DECIMAL(10, 2),
                                lucro_total DECIMAL(10, 2)
                            );
                        """
                    )
                except Exception as e:
                    logging.error(
                        f"Erro ao criar a tabela temporária {entity_key}: {e}"
                    )
                    raise

        conn_id = (
            "postgres_staging_area"
            if entity_key != "fato_vendas"
            else "postgres_data_warehouse"
        )

        process_table(
            sql_query=entity[f"query_sql_{entity_key}"],
            destination_table=f"schema_dw.{entity_key}",
            target_fields=entity["fields"],
            conn_id=conn_id,
        )

        if entity_key == "fato_vendas":
            with postgres_connection("postgres_data_warehouse") as dw_hook:
                logging.info("Deletando tabela temporária fato_vendas_temp.")
                try:
                    dw_hook.run(sql="DROP TABLE IF EXISTS schema_dw.fato_vendas_temp")
                except Exception as e:
                    logging.error(
                        f"Erro ao deletar a tabela temporária fato_vendas_temp: {e}"
                    )
                    raise

        logging.info(f"{entity_type.capitalize()} {entity_key} processada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao processar a {entity_type} {entity_key}: {e}")
        raise


with DAG(
    dag_id="pipeline_dw",
    description="Esta DAG é responsável por processar e carregar os dados da Staging Area para o Data Warehouse",
    start_date=pendulum.datetime(2024, 11, 30, tz="UTC"),
    schedule="0 * * * *",
    default_args=default_args,
    catchup=False,
) as dag:
    tuple_tables = [
        ("dim_produto", "dimensao"),
        ("dim_cliente", "dimensao"),
        ("dim_localidade", "dimensao"),
        ("dim_tempo", "dimensao"),
        ("dim_loja", "dimensao"),
        ("dim_canal_venda", "dimensao"),
        ("dim_vendedor", "dimensao"),
        ("fato_vendas_temp", "fato"),
        ("fato_vendas", "fato"),
    ]

    tasks = []
    for dim in tuple_tables:
        task = PythonOperator(
            task_id=f"task_processar_{dim[0]}",
            python_callable=process_entity,
            op_args=[dim[0], dim[1]],
        )
        tasks.append(task)

    for i in range(len(tasks) - 1):
        tasks[i] >> tasks[i + 1]

    send_email = EmailOperator(
        task_id="enviar_email_sucesso",
        to="kjonnathas@gmail.com",
        subject="Pipeline DW",
        html_content="""
        <p>A DAG <strong>pipeline_dw</strong> foi concluída sem erros.</p>
        <p>Verifique os logs para mais detalhes, se necessário.</p>
        """,
    )

    tasks[-1] >> send_email
