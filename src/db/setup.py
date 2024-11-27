import sqlite3

# Definição das tabelas
CREATE_TABLES = [
    """
    CREATE TABLE IF NOT EXISTS fixtures (
        fixture_id INTEGER PRIMARY KEY,
        league_id INTEGER NOT NULL,
        season INTEGER NOT NULL,
        date TEXT NOT NULL,
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
        venue_id INTEGER
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
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Criar as tabelas
    for table_sql in CREATE_TABLES:
        cursor.execute(table_sql)

    # Confirmar as alterações e fechar a conexão
    connection.commit()
    connection.close()

if __name__ == "__main__":
    print("Criando o banco de dados e as tabelas...")
    create_database()
    print("Banco de dados configurado com sucesso!")
