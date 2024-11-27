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

from config.settings import DB_PATH

def get_stored_fixture_ids(league_id, season, db_path=DB_PATH):
    """
    Retorna uma lista de fixture_ids já armazenados no banco para uma liga e temporada específicas.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT fixture_id FROM fixtures
            WHERE league_id = ? AND season = ?
        """, (league_id, season))

        result = [row[0] for row in cursor.fetchall()]
        connection.close()
        return result
    except Exception as e:
        raise RuntimeError(f"Erro ao consultar fixtures no banco: {e}")

def get_stored_team_ids(league_id, db_path="data/db/database.sqlite"):
    """
    Retorna uma lista de team_ids já armazenados no banco para uma liga específica.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT DISTINCT team_id FROM teams
            WHERE team_id IN (
                SELECT DISTINCT home_team_id FROM fixtures WHERE league_id = ?
                UNION
                SELECT DISTINCT away_team_id FROM fixtures WHERE league_id = ?
            )
        """, (league_id, league_id))

        result = [row[0] for row in cursor.fetchall()]
        connection.close()
        return result
    except Exception as e:
        raise RuntimeError(f"Erro ao consultar times no banco: {e}")
    