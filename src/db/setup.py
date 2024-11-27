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

from src.utils.logger import log_message

LOG_FILE = "data/logs/setup.log"

# Definição das tabelas
CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS fixtures (
        fixture_id INTEGER PRIMARY KEY,
        league_id INTEGER NOT NULL,
        season INTEGER NOT NULL,
        date TEXT NOT NULL,
        timestamp INTEGER,
        venue_id INTEGER,
        referee TEXT,
        home_team_id INTEGER NOT NULL,
        away_team_id INTEGER NOT NULL,
        home_goals INTEGER,
        away_goals INTEGER,
        halftime_home_goals INTEGER,
        halftime_away_goals INTEGER
    );

    """,
    """
    CREATE TABLE IF NOT EXISTS teams (
        team_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT,
        founded INTEGER,
        venue_id INTEGER,
        FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS venues (
        venue_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT,
        capacity INTEGER,
        surface TEXT
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fixture_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        player_id INTEGER,
        event_type TEXT NOT NULL,
        event_detail TEXT,
        time_elapsed INTEGER,
        FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id),
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS statistics (
        statistic_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fixture_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        shots_on_goal INTEGER,
        shots_off_goal INTEGER,
        possession_percentage REAL,
        passes_completed INTEGER,
        FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id),
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS player_statistics (
        player_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fixture_id INTEGER NOT NULL,
        player_id INTEGER NOT NULL,
        team_id INTEGER NOT NULL,
        minutes_played INTEGER,
        goals_scored INTEGER,
        assists INTEGER,
        yellow_cards INTEGER,
        red_cards INTEGER,
        FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id),
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
    );
    """
]

def create_database(db_path="data/db/database.sqlite"):
    """
    Conecta ao banco de dados SQLite e cria as tabelas necessárias.
    """
    try:
        # Iniciar log
        log_message("INFO", "Iniciando configuração do banco de dados...", LOG_FILE, to_console=True)
        
        # Garante que o diretório do banco de dados exista
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)

        # Conectar ao banco
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Criar tabelas
        for table_sql in CREATE_TABLES:
            cursor.execute(table_sql)

        # Confirmar alterações
        connection.commit()
        connection.close()

        # Log de sucesso
        log_message("INFO", f"Banco de dados configurado com sucesso em {db_path}", LOG_FILE, to_console=True)

    except Exception as e:
        # Log de erro
        log_message("ERROR", f"Erro ao configurar o banco de dados: {str(e)}", LOG_FILE, to_console=True)
        raise


if __name__ == "__main__":
    create_database()
