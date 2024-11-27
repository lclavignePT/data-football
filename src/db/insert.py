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

def insert_fixtures(fixtures, db_path=DB_PATH):
    """
    Insere dados de fixtures no banco de dados.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        for fixture in fixtures:
            cursor.execute("""
                INSERT INTO fixtures (
                    fixture_id, league_id, season, date, timestamp, venue_id, referee,
                    home_team_id, away_team_id, home_goals, away_goals, halftime_home_goals, halftime_away_goals
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(fixture_id) DO NOTHING
            """, (
                fixture["fixture_id"], fixture["league_id"], fixture["season"], fixture["date"],
                fixture["timestamp"], fixture["venue_id"], fixture["referee"],
                fixture["home_team_id"], fixture["away_team_id"], fixture["home_goals"], fixture["away_goals"],
                fixture["halftime_home_goals"], fixture["halftime_away_goals"]
            ))
        connection.commit()
        connection.close()
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir fixtures: {e}")
    
def insert_teams(teams, db_path=DB_PATH):
    """
    Insere dados de times no banco de dados.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        for team in teams:
            cursor.execute("""
                INSERT INTO teams (team_id, name, country, founded, venue_id)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(team_id) DO NOTHING
            """, (
                team["team_id"], team["name"], team["country"], team["founded"], team["venue_id"]
            ))
        connection.commit()
        connection.close()
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir times: {e}")

