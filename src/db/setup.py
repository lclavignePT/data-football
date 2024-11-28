import sqlite3
import os
import sys
from pathlib import Path

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from utils.logger import log_message
from config.settings import DB_PATH

LOG_FILE = BASE_DIR / "data/logs/setup_DB.log"
sql_file_path = BASE_DIR / "config/database.sql"

def create_database(db_path, sql_file_path):
    """
    Conecta ao banco de dados SQLite e cria as tabelas necessárias.
    """
    connection = None
    try:
        # Iniciar log
        log_message("INFO", "Iniciando configuração do banco de dados...", LOG_FILE, to_console=True)
        
        # Garante que o diretório do banco de dados exista
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        # Verificar se o arquivo SQL existe
        if not os.path.exists(sql_file_path):
            log_message("ERROR", f"Arquivo SQL não encontrado: {sql_file_path}", LOG_FILE, to_console=True)
            raise FileNotFoundError(f"Arquivo SQL não encontrado: {sql_file_path}")

        # Conectar ao banco
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Leitura do arquivo SQL
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        cursor.executescript(sql_script)

        # Log de sucesso
        log_message("INFO", f"Banco de dados configurado com sucesso em {db_path}", LOG_FILE, to_console=True)

    except Exception as e:
        # Log de erro
        log_message("ERROR", f"Erro ao configurar o banco de dados: {str(e)}", LOG_FILE, to_console=True)
        raise
    finally:
        # Fechar conexão
        if connection:
            connection.close()

if __name__ == "__main__":
    create_database(DB_PATH, sql_file_path)
