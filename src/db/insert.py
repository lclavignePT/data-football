import sqlite3

def insert_fixtures(fixtures, db_path="data/db/database.sqlite"):
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
