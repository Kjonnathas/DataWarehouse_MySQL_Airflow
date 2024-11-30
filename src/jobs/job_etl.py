import mysql.connector
from mysql.connector import Error
from mysql.connector.connection_cext import CMySQLConnection
from dotenv import load_dotenv
import os
import csv
import logging
from datetime import datetime
from typing import Iterator, Optional
from config_models import tables_config
import unicodedata

# Variáveis de data
date = datetime.today()
day = date.day
month = date.month
year = date.year

# Carrega as variáveis do arquivo .env
load_dotenv()

# Acessa as variáveis de ambiente
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
db = os.getenv("MYSQL_DB")
folder = os.getenv("FOLDER_PATH")
logs = os.getenv("FOLDER_LOGS")

# Configurar o logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename=os.path.join(logs, f"job_etl_{day}_{month}_{year}.log"),
    filemode="a",
)


def normalize_text(text: str) -> str:
    """
    Remove acentos de uma string e a retorna normalizada.

    Parâmetros:
    - text (str): O texto que será normalizado.

    Retorna:
    - str: O texto sem acentos.
    """
    if not isinstance(text, str):
        return text

    # Normaliza a string para forma NFD (decomposição de caracteres)
    normalized = unicodedata.normalize("NFD", text)

    # Remove caracteres diacríticos (acentos)
    without_accent = "".join(
        char for char in normalized if unicodedata.category(char) != "Mn"
    )

    # Retorna a string normalizada na forma NFC (composição de caracteres)
    return unicodedata.normalize("NFC", without_accent)


def read_files(folder_path: str, file_name: str) -> Optional[Iterator[list]]:
    """
    Lê o conteúdo de um arquivo CSV em uma pasta especificada.

    Args
    ----
    folder_path : str
        Caminho da pasta onde o arquivo CSV está localizado.
    file_name : str
        Nome do arquivo CSV que será lido.

    Returns
    -------
    Optional[Iterator[list]]
        Um iterador contendo as linhas do arquivo CSV como listas,
        ou None se ocorrer um erro durante a leitura.

    Raises
    ------
    FileNotFoundError
        Se o arquivo especificado não for encontrado no caminho fornecido.
    PermissionError
        Se não houver permissões para acessar o arquivo.
    ValueError
        Se o arquivo não estiver no formato esperado.
    """

    try:
        file_path = os.path.join(folder_path, file_name)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        with open(file_path, mode="r", encoding="Latin-1") as file:
            reader = csv.reader(file, delimiter=";")

            next(reader)

            data = [[normalize_text(_) for _ in row] for row in reader]

            logging.info(f"Leitura do arquivo {file_name} realizada com sucesso.")

            return data

    except FileNotFoundError as fnf_error:
        logging.error(f"Arquivo não encontrado: {fnf_error}")

        return None

    except PermissionError as perm_error:
        logging.error(f"Permissões insuficientes para acessar o arquivo: {perm_error}")

        return None

    except ValueError as val_error:
        logging.error(f"Erro de valor ao processar o arquivo: {val_error}")

        return None

    except Exception as e:
        logging.error(
            f"Ocorreu um erro inesperado durante a leitura do arquivo {file_name}.\n\nErro: {e}"
        )

        return None


def connection_database(
    host: str, port: str, user: str, password: str, db: str = None
) -> CMySQLConnection | None:
    """
    Cria e retorna a conexão com o banco de dados MySQL.

    A função estabelece uma conexão com o banco de dados MySQL e, caso um banco de dados não seja informado, cria um banco
    de dados com o nome especificado no parâmetro `database`. Também ajusta o conjunto de caracteres do banco para `utf8mb4`.

    Args
    -----
    host : str
        Hostname do servidor onde o banco de dados está localizado.
    port : str
        Porta de conexão ao banco de dados.
    user : str
        Usuário para autenticação no banco de dados.
    password : str
        Senha para autenticação no banco de dados.
    database : str, opcional
        Nome do banco de dados. Se não informado, será criado durante a execução.

    Returns
    --------
    CMySQLConnection:
        Objeto de conexão ao banco de dados MySQL. Caso ocorra um erro, retorna `None`.

    Raises
    -------
    Error:
        Lança um erro caso a conexão ou execução de comandos SQL falhe.
    """

    conn = mysql.connector.connect(host=host, port=port, user=user, password=password)

    try:
        if conn.is_connected():
            logging.info("A conexão com o banco de dados foi estabelecida com sucesso!")

            if db is not None:
                with conn.cursor() as cursor:
                    create_db = f"CREATE DATABASE IF NOT EXISTS {db}"

                    cursor.execute(create_db)

                    alter_db_charset = f"ALTER DATABASE {db} CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci"

                    cursor.execute(alter_db_charset)

                    conn.database = db

            return conn, db

    except Error as e:
        logging.error(
            f"Não foi possível estabelecer a conexão com o banco de dados devido ao seguinte erro:\n\n{e}"
        )

        return None


def create_table_and_insert_data(conn: CMySQLConnection, db: str) -> None:
    """
    Cria uma tabela no banco de dados e insere os dados do arquivo CSV correspondente.

    Args:
        conn: Conexão com o banco de dados.
        db: Nome do banco de dados.
    """

    def format_date(date_str: str) -> Optional[str]:
        """
        Converte a data para o formato YYYY-MM-DD, aceitando entradas nos formatos DD/MM/YYYY ou YYYY-MM-DD.

        Args:
            date_str: Data em formato string.

        Returns:
            Data formatada no padrão YYYY-MM-DD ou None se a data for inválida.
        """
        for date_format in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(date_str, date_format).strftime("%Y-%m-%d")
            except ValueError:
                continue

        return None

    if conn:
        try:
            with conn.cursor() as cursor:
                dict_models = tables_config()
                for model in dict_models.keys():
                    for file in os.listdir(folder):
                        if file.endswith(".csv"):
                            table_name = os.path.basename(os.path.join(folder, file))[
                                :-4
                            ]
                            if table_name != model:
                                continue
                            else:
                                table_schema = dict_models[table_name]["schema"]

                                columns = dict_models[table_name]["columns"]

                                create_table_query = f"CREATE TABLE IF NOT EXISTS {db}.{table_name} ({table_schema})"
                                cursor.execute(create_table_query)
                                logging.info(
                                    f"Tabela {table_name} criada ou já existe."
                                )

                                data = read_files(folder, file)
                                if data is None:
                                    logging.warning(
                                        f"Arquivo {file} não encontrado ou vazio."
                                    )
                                    return None

                                data_tuple = []
                                for row in data:
                                    processed_row = []
                                    for index, value in enumerate(row[: len(columns)]):
                                        if (
                                            "date" in columns[index].lower()
                                            or "dt_" in columns[index].lower()
                                        ):
                                            if value is None or value == "":
                                                processed_row.append(None)
                                            else:
                                                formatted_date = format_date(value)
                                                if not formatted_date:
                                                    logging.warning(
                                                        f"Data inválida '{value}' encontrada no arquivo {file} na tabela {table_name}."
                                                    )
                                                    processed_row.append(None)
                                                else:
                                                    processed_row.append(formatted_date)
                                        else:
                                            processed_row.append(value)
                                    data_tuple.append(tuple(processed_row))

                                insert_query = f"INSERT INTO {db}.{table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
                                batch_size = 50000
                                for i in range(0, len(data_tuple), batch_size):
                                    current_batch = data_tuple[i : i + batch_size]
                                    cursor.executemany(insert_query, current_batch)
                                    logging.info(
                                        f"Batch de {len(current_batch)} registros inseridos na tabela {table_name}."
                                    )

                                logging.info(
                                    f"Dados inseridos com sucesso na tabela {table_name}."
                                )

            conn.commit()

        except Exception as e:
            logging.error(
                f"Erro ao criar ou inserir dados na tabela {table_name}.\n\nErro: {e}"
            )
            conn.rollback()

        finally:
            conn.close()


if __name__ == "__main__":
    conn = connection_database(
        host=host, port=port, user=user, password=password, db=db
    )
    create_table_and_insert_data(conn[0], conn[1])
