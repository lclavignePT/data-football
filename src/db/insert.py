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

def insert_fixtures_ids(fixtures, db_path=DB_PATH):
    """
    Insere dados na tabela fixtures_id_processed no banco de dados.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        for fixture in fixtures:
            cursor.execute("""
                INSERT INTO fixtures_id_processed (
                    fixture_id, timestamp, processed
                )
                VALUES (?, ?, 0)
                ON CONFLICT(fixture_id) DO NOTHING
            """, (
                fixture["fixture_id"],
                fixture["timestamp"]
            ))
        connection.commit()
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir fixtures_id_processed: {e}")
    finally:
        if connection:
            connection.close()
    
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

def insert_venue(data, db_path=DB_PATH):
    """
    Insere um venue na tabela venues.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO venues (venue_id, name, capacity, city, surface)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(venue_id) DO NOTHING
        """, (
            data["venue_id"], data["name"], data["capacity"],
            data["city"], data["surface"]
        ))

        connection.commit()
        connection.close()
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir venue: {e}")

def insert_fixture(fixture, db_path=DB_PATH):
    """
    Insere os dados de um fixture na tabela fixtures.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

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
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir fixture: {e}")
    finally:
        connection.close()

def insert_fixture_events(events, db_path=DB_PATH):
    """
    Insere os eventos de um fixture na tabela fixture_events.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        for event in events:
            cursor.execute("""
                INSERT INTO fixture_events (
                    fixture_id, team_id, player_id, event_type, event_detail, time_elapsed, time_extra
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                event["fixture_id"], event["team_id"], event["player_id"],
                event["event_type"], event["event_detail"], event["time_elapsed"], event["time_extra"]
            ))

        connection.commit()
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir eventos: {e}")
    finally:
        connection.close()

def insert_team_statistics(team_statistics, db_path=DB_PATH):
    """
    Insere as estatísticas de times na tabela fixture_team_statistics.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        for stats in team_statistics:
            cursor.execute("""
                INSERT INTO fixture_team_statistics (
                    fixture_id, team_id, shots_on_goal, shots_off_goal, total_shots, blocked_shots,
                    shots_insidebox, shots_outsidebox, fouls, corner_kicks, offsides, ball_possession,
                    yellow_cards, red_cards, goalkeeper_saves, total_passes, passes_accurate,
                    passes_percentage_accurate, expected_goals, goals_prevented
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                stats["fixture_id"], stats["team_id"], stats["shots_on_goal"], stats["shots_off_goal"],
                stats["total_shots"], stats["blocked_shots"], stats["shots_insidebox"], stats["shots_outsidebox"],
                stats["fouls"], stats["corner_kicks"], stats["offsides"], stats["ball_possession"],
                stats["yellow_cards"], stats["red_cards"], stats["goalkeeper_saves"],
                stats["total_passes"], stats["passes_accurate"], stats["passes_percentage_accurate"],
                stats["expected_goals"], stats["goals_prevented"]
            ))

        connection.commit()
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir estatísticas de time: {e}")
    finally:
        connection.close()

def insert_start_xi(start_xi, db_path=DB_PATH):
    """
    Insere os dados de titulares na tabela fixture_startXI.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        for player in start_xi:
            cursor.execute("""
                INSERT INTO fixture_startXI (
                    fixture_id, team_id, coach_id, formation, player_id, player_number, position, grid
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                player["fixture_id"], player["team_id"], player["coach_id"], player["formation"],
                player["player_id"], player["player_number"], player["position"], player["grid"]
            ))

        connection.commit()
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir titulares: {e}")
    finally:
        connection.close()

def insert_substitutes(substitutes, db_path=DB_PATH):
    """
    Insere os dados de substitutos na tabela fixture_substitutes.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        for substitute in substitutes:
            cursor.execute("""
                INSERT INTO fixture_substitutes (
                    fixture_id, team_id, coach_id, player_id, player_number, position
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                substitute["fixture_id"], substitute["team_id"], substitute["coach_id"],
                substitute["player_id"], substitute["player_number"], substitute["position"]
            ))

        connection.commit()
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir substitutos: {e}")
    finally:
        connection.close()

def insert_player_statistics(player_statistics, db_path=DB_PATH):
    """
    Insere as estatísticas de jogadores na tabela fixture_player_statistics.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        for stats in player_statistics:
            cursor.execute("""
                INSERT INTO fixture_player_statistics (
                    fixture_id, player_id, team_id, minutes_played, player_number, position,
                    rating, captain, substitute, offsides, shots_total, shots_on_target,
                    goals_scored, goals_conceded, assists, saves, passes_total, passes_key,
                    passes_accuracy, tackles_total, tackles_blocks, tackles_interceptions,
                    duels_total, duels_won, dribbles_attempts, dribbles_success, dribbles_past,
                    fouls_drawn, fouls_committed, yellow_cards, red_cards, penalties_won,
                    penalties_committed, penalties_scored, penalties_missed, penalties_saved
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                stats["fixture_id"], stats["player_id"], stats["team_id"], stats["minutes_played"],
                stats["player_number"], stats["position"], stats["rating"], stats["captain"],
                stats["substitute"], stats["offsides"], stats["shots_total"], stats["shots_on_target"],
                stats["goals_scored"], stats["goals_conceded"], stats["assists"], stats["saves"],
                stats["passes_total"], stats["passes_key"], stats["passes_accuracy"],
                stats["tackles_total"], stats["tackles_blocks"], stats["tackles_interceptions"],
                stats["duels_total"], stats["duels_won"], stats["dribbles_attempts"], stats["dribbles_success"],
                stats["dribbles_past"], stats["fouls_drawn"], stats["fouls_committed"], stats["yellow_cards"],
                stats["red_cards"], stats["penalties_won"], stats["penalties_committed"],
                stats["penalties_scored"], stats["penalties_missed"], stats["penalties_saved"]
            ))

        connection.commit()
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir estatísticas de jogador: {e}")
    finally:
        connection.close()
