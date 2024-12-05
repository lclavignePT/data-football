CREATE TABLE fixtures (
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
CREATE TABLE fixtures_id_processed (
    fixture_id INTEGER PRIMARY KEY,
    timestamp INTEGER,
    processed BOOLEAN DEFAULT 0 NOT NULL,
    FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id)
);
CREATE TABLE teams (
    team_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    country TEXT,
    founded INTEGER,
    venue_id INTEGER,
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);
CREATE TABLE venues (
    venue_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    city TEXT,
    capacity INTEGER,
    surface TEXT
);
CREATE TABLE players (
    player_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE coachs (
    coach_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE fixture_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fixture_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    player_id INTEGER,
    event_type TEXT NOT NULL,
    event_detail TEXT,
    time_elapsed INTEGER,
    time_extra INTEGER,
    FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE fixture_team_statistics (
    statistic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fixture_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    shots_on_goal INTEGER NOT NULL DEFAULT 0,
    shots_off_goal INTEGER NOT NULL DEFAULT 0,
    total_shots INTEGER NOT NULL DEFAULT 0,
    blocked_shots INTEGER NOT NULL DEFAULT 0,
    shots_insidebox INTEGER NOT NULL DEFAULT 0,
    shots_outsidebox INTEGER NOT NULL DEFAULT 0,
    fouls INTEGER NOT NULL DEFAULT 0,
    corner_kicks INTEGER NOT NULL DEFAULT 0,
    offsides INTEGER NOT NULL DEFAULT 0,
    ball_possession REAL NOT NULL DEFAULT 0,
    yellow_cards INTEGER NOT NULL DEFAULT 0,
    red_cards INTEGER NOT NULL DEFAULT 0,
    goalkeeper_saves INTEGER NOT NULL DEFAULT 0,
    total_passes INTEGER NOT NULL DEFAULT 0,
    passes_accurate INTEGER NOT NULL DEFAULT 0,
    passes_percentage_accurate REAL NOT NULL DEFAULT 0,
    expected_goals REAL NOT NULL DEFAULT 0,
    goals_prevented INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);
CREATE TABLE fixture_player_statistics (
    player_stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fixture_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    minutes_played INTEGER NOT NULL DEFAULT 0,
    player_number INTEGER NOT NULL DEFAULT 0,
    position TEXT NOT NULL,
    rating REAL NOT NULL DEFAULT 0.0,
    captain BOOLEAN NOT NULL DEFAULT 0,
    substitute BOOLEAN NOT NULL DEFAULT 0,
    offsides INTEGER NOT NULL DEFAULT 0,
    shots_total INTEGER NOT NULL DEFAULT 0,
    shots_on_target INTEGER NOT NULL DEFAULT 0,
    goals_scored INTEGER NOT NULL DEFAULT 0,
    goals_conceded INTEGER NOT NULL DEFAULT 0,
    assists INTEGER NOT NULL DEFAULT 0,
    saves INTEGER NOT NULL DEFAULT 0,
    passes_total INTEGER NOT NULL DEFAULT 0,
    passes_key INTEGER NOT NULL DEFAULT 0,
    passes_accuracy REAL NOT NULL DEFAULT 0.0,
    tackles_total INTEGER NOT NULL DEFAULT 0,
    tackles_blocks INTEGER NOT NULL DEFAULT 0,
    tackles_interceptions INTEGER NOT NULL DEFAULT 0,
    duels_total INTEGER NOT NULL DEFAULT 0,
    duels_won INTEGER NOT NULL DEFAULT 0,
    dribbles_attempts INTEGER NOT NULL DEFAULT 0,
    dribbles_success INTEGER NOT NULL DEFAULT 0,
    dribbles_past INTEGER NOT NULL DEFAULT 0,
    fouls_drawn INTEGER NOT NULL DEFAULT 0,
    fouls_committed INTEGER NOT NULL DEFAULT 0,
    yellow_cards INTEGER NOT NULL DEFAULT 0,
    red_cards INTEGER NOT NULL DEFAULT 0,
    penalties_won INTEGER NOT NULL DEFAULT 0,
    penalties_committed INTEGER NOT NULL DEFAULT 0,
    penalties_scored INTEGER NOT NULL DEFAULT 0,
    penalties_missed INTEGER NOT NULL DEFAULT 0,
    penalties_saved INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
CREATE TABLE fixture_startXI (
    start_xi_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fixture_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    coach_id INTEGER NOT NULL,
    formation TEXT,
    player_id INTEGER NOT NULL,
    player_number INTEGER NOT NULL,
    position TEXT NOT NULL,
    grid TEXT,
    FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (coach_id) REFERENCES coachs(coach_id)
);
CREATE TABLE fixture_substitutes (
    sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fixture_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    coach_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    player_number INTEGER NOT NULL,
    position TEXT NOT NULL,
    FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (coach_id) REFERENCES coachs(coach_id)
);
CREATE INDEX idx_fixtures_league_season ON fixtures (league_id, season);
CREATE INDEX idx_fixtures_home_team ON fixtures (home_team_id);
CREATE INDEX idx_fixtures_away_team ON fixtures (away_team_id);
CREATE INDEX idx_fixtures_date ON fixtures (date);
CREATE INDEX idx_fixtures_timestamp ON fixtures (timestamp);
CREATE INDEX idx_fixtures_id_processed_status ON fixtures_id_processed (processed, timestamp);
CREATE INDEX idx_teams_name ON teams (name);
CREATE INDEX idx_teams_country ON teams (country);
CREATE INDEX idx_players_name ON players (name);
CREATE INDEX idx_fixture_events_fixture_team ON fixture_events (fixture_id, team_id);
CREATE INDEX idx_fixture_events_player ON fixture_events (player_id);
CREATE INDEX idx_fixture_events_type ON fixture_events (event_type, event_detail);
CREATE INDEX idx_fixture_events_time ON fixture_events (time_elapsed);
CREATE INDEX idx_team_statistics_fixture ON fixture_team_statistics (fixture_id, team_id);
CREATE INDEX idx_team_statistics_expected_goals ON fixture_team_statistics (expected_goals);
CREATE INDEX idx_player_statistics_fixture ON fixture_player_statistics (fixture_id, player_id, team_id);
CREATE INDEX idx_player_statistics_rating ON fixture_player_statistics (rating);
CREATE INDEX idx_startXI_fixture_team ON fixture_startXI (fixture_id, team_id);
CREATE INDEX idx_startXI_player ON fixture_startXI (player_id);
CREATE INDEX idx_substitutes_fixture_team ON fixture_substitutes (fixture_id, team_id);
CREATE INDEX idx_substitutes_player ON fixture_substitutes (player_id);
CREATE TABLE odds (
    odd_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fixture_id INTEGER NOT NULL,
    home_win REAL,
    draw REAL,
    away_win REAL,
    over_0_5 REAL,
    under_0_5 REAL,
    over_1_5 REAL,
    under_1_5 REAL,
    over_2_5 REAL,
    under_2_5 REAL,
    over_3_5 REAL,
    under_3_5 REAL,
    over_4_5 REAL,
    under_4_5 REAL,
    over_5_5 REAL,
    under_5_5 REAL,
    over_6_5 REAL,
    under_6_5 REAL,
    updated_at TIMESTAMP,
    FOREIGN KEY (fixture_id) REFERENCES fixtures(fixture_id) ON DELETE CASCADE
);
CREATE UNIQUE INDEX idx_odds_fixture_id ON odds(fixture_id);
