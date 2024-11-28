class UpdateFixtureService:
    @staticmethod
    def process_fixture_data(data):
        """
        Processa o JSON retornado pela API para separar os dados por tabela.
        """
        # Validar e acessar o primeiro elemento da lista 'response'
        if not data.get("response"):
            raise ValueError("A chave 'response' está ausente ou está vazia no JSON.")

        fixture_data = data["response"][0]

        # Processar dados usando os métodos atualizados
        processed_data = {
            "fixtures": UpdateFixtureService._process_fixture(fixture_data),
            "events": UpdateFixtureService._process_events(fixture_data.get("events", []), fixture_data.get("fixture", {}).get("id")),
            "team_statistics": UpdateFixtureService._process_team_statistics(
                fixture_data.get("statistics", []), fixture_data.get("fixture", {}).get("id")
            ),
            "lineups": UpdateFixtureService._process_lineups(fixture_data.get("lineups", []), fixture_data.get("fixture", {}).get("id")),
            "player_statistics": UpdateFixtureService._process_player_statistics(
                fixture_data.get("players", []), fixture_data.get("fixture", {}).get("id")
            ),
        }

        return processed_data

    @staticmethod
    def _process_fixture(fixture_data):
        """
        Processa os dados da partida para inserir na tabela 'fixtures'.
        """
        fixture = fixture_data.get("fixture", {})
        league = fixture_data.get("league", {})
        teams = fixture_data.get("teams", {})
        goals = fixture_data.get("goals", {})
        score = fixture_data.get("score", {})
        venue = fixture.get("venue", {})

        return {
            "fixture_id": fixture.get("id"),
            "league_id": league.get("id"),
            "season": league.get("season"),
            "date": fixture.get("date"),
            "timestamp": fixture.get("timestamp"),
            "venue_id": venue.get("id"),
            "referee": fixture.get("referee"),
            "home_team_id": teams.get("home", {}).get("id"),
            "away_team_id": teams.get("away", {}).get("id"),
            "home_goals": goals.get("home"),
            "away_goals": goals.get("away"),
            "halftime_home_goals": score.get("halftime", {}).get("home"),
            "halftime_away_goals": score.get("halftime", {}).get("away"),
        }

    @staticmethod
    def _process_events(events, fixture_id):
        """
        Processa a seção 'events' do JSON.
        """
        processed_events = []

        if not events:
            return processed_events  # Retorna lista vazia se eventos estiverem ausentes

        for event in events:
            processed_events.append({
                "event_id": None,  # Será autoincrementado no banco de dados
                "fixture_id": fixture_id,
                "team_id": event.get("team", {}).get("id"),
                "player_id": event.get("player", {}).get("id"),
                "assist_id": event.get("assist", {}).get("id"),
                "event_type": event.get("type"),
                "event_detail": event.get("detail"),
                "time_elapsed": event.get("time", {}).get("elapsed"),
                "time_extra": event.get("time", {}).get("extra"),
            })
        return processed_events

    @staticmethod
    def _process_team_statistics(statistics, fixture_id):
        def parse_percentage(value):
            try:
                return float(value.replace("%", "")) / 100 if value else 0.0
            except (ValueError, AttributeError):
                return 0.0

        def parse_int(value):
            try:
                return int(value) if value is not None else 0
            except (ValueError, TypeError):
                return 0

        def parse_float(value):
            try:
                return float(value) if value is not None else 0.0
            except (ValueError, TypeError):
                return 0.0

        processed_stats = []
        for team_stats in statistics:
            team = team_stats.get("team", {})
            stats_list = team_stats.get("statistics", [])
            stats = {stat.get("type"): stat.get("value") for stat in stats_list}

            # Obter valores, garantindo que sejam do tipo correto
            expected_goals = parse_float(stats.get("Expected Goals"))
            goals_prevented = parse_float(stats.get("Goals Prevented"))

            processed_stats.append({
                "fixture_id": fixture_id,
                "team_id": team.get("id"),
                "shots_on_goal": parse_int(stats.get("Shots on Goal")),
                "shots_off_goal": parse_int(stats.get("Shots off Goal")),
                "total_shots": parse_int(stats.get("Total Shots")),
                "blocked_shots": parse_int(stats.get("Blocked Shots")),
                "shots_insidebox": parse_int(stats.get("Shots insidebox")),
                "shots_outsidebox": parse_int(stats.get("Shots outsidebox")),
                "fouls": parse_int(stats.get("Fouls")),
                "corner_kicks": parse_int(stats.get("Corner Kicks")),
                "offsides": parse_int(stats.get("Offsides")),
                "ball_possession": parse_percentage(stats.get("Ball Possession")),
                "yellow_cards": parse_int(stats.get("Yellow Cards")),
                "red_cards": parse_int(stats.get("Red Cards")),  # Corrigido para usar parse_int
                "goalkeeper_saves": parse_int(stats.get("Goalkeeper Saves")),
                "total_passes": parse_int(stats.get("Total passes")),
                "passes_accurate": parse_int(stats.get("Passes accurate")),
                "passes_percentage_accurate": parse_percentage(stats.get("Passes %")),
                "expected_goals": expected_goals,
                "goals_prevented": goals_prevented,
            })
        return processed_stats


    @staticmethod
    def _process_lineups(lineups, fixture_id):
        """
        Processa a seção 'lineups' do JSON para as tabelas 'fixture_startXI' e 'fixture_substitutes'.
        """
        start_xi_data = []
        substitutes_data = []

        if not lineups:
            return {"start_xi": start_xi_data, "substitutes": substitutes_data}

        for lineup in lineups:
            team = lineup.get("team", {})
            coach = lineup.get("coach", {})
            formation = lineup.get("formation")

            # Processar titulares (startXI)
            for player in lineup.get("startXI", []):
                player_data = player.get("player", {})
                start_xi_data.append({
                    "fixture_id": fixture_id,
                    "team_id": team.get("id"),
                    "coach_id": coach.get("id", 100000) or 100000,
                    "formation": formation,
                    "player_id": player_data.get("id"),
                    "player_number": player_data.get("number"),
                    "position": player_data.get("pos", "X") or "X",
                    "grid": player_data.get("grid"),
                })

            # Processar substitutos
            for substitute in lineup.get("substitutes", []):
                player_data = substitute.get("player", {})
                substitutes_data.append({
                    "fixture_id": fixture_id,
                    "team_id": team.get("id"),
                    "coach_id": coach.get("id", 100000) or 100000,
                    "player_id": player_data.get("id"),
                    "player_number": player_data.get("number"),
                    "position": player_data.get("pos", "X") or "X",
                })

        return {
            "start_xi": start_xi_data,
            "substitutes": substitutes_data
        }

    @staticmethod
    def _process_player_statistics(players, fixture_id):
        """
        Processa a seção 'players' do JSON para a tabela 'fixture_player_statistics'.
        """
        def parse_int(value):
            """
            Tenta converter o valor para int. Se falhar ou for None, retorna 0.
            """
            try:
                return int(value) if value is not None else 0
            except (ValueError, TypeError):
                return 0

        def parse_float(value):
            """
            Tenta converter o valor para float. Se falhar ou for None, retorna 0.0.
            """
            try:
                return float(value) if value is not None else 0.0
            except (ValueError, TypeError):
                return 0.0

        processed_players = []

        for team_data in players:
            team_id = team_data.get("team", {}).get("id")
            for player_info in team_data.get("players", []):
                player = player_info.get("player", {})
                statistics = player_info.get("statistics", [{}])[0]  # Pode haver múltiplas entradas, pegamos a primeira

                # Obter estatísticas específicas
                games_stats = statistics.get("games", {})
                shots_stats = statistics.get("shots", {})
                goals_stats = statistics.get("goals", {})
                passes_stats = statistics.get("passes", {})
                tackles_stats = statistics.get("tackles", {})
                duels_stats = statistics.get("duels", {})
                dribbles_stats = statistics.get("dribbles", {})
                fouls_stats = statistics.get("fouls", {})
                cards_stats = statistics.get("cards", {})
                penalty_stats = statistics.get("penalty", {})

                try:
                    processed_player = {
                        "fixture_id": fixture_id,
                        "player_id": player.get("id"),
                        "team_id": team_id,
                        "minutes_played": parse_int(games_stats.get("minutes", 0)),
                        "player_number": parse_int(player.get("number", 0)),
                        "position": games_stats.get("position", "N/A"),
                        "rating": parse_float(games_stats.get("rating", 0.0)),
                        "captain": games_stats.get("captain", False),
                        "substitute": games_stats.get("substitute", False),
                        "offsides": parse_int(statistics.get("offsides", 0)),
                        "shots_total": parse_int(shots_stats.get("total", 0)),
                        "shots_on_target": parse_int(shots_stats.get("on", 0)),
                        "goals_scored": parse_int(goals_stats.get("total", 0)),
                        "goals_conceded": parse_int(goals_stats.get("conceded", 0)),
                        "assists": parse_int(goals_stats.get("assists", 0)),
                        "saves": parse_int(statistics.get("saves", 0)),
                        "passes_total": parse_int(passes_stats.get("total", 0)),
                        "passes_key": parse_int(passes_stats.get("key", 0)),
                        "passes_accuracy": parse_float(passes_stats.get("accuracy", 0.0)),
                        "tackles_total": parse_int(tackles_stats.get("total", 0)),
                        "tackles_blocks": parse_int(tackles_stats.get("blocks", 0)),
                        "tackles_interceptions": parse_int(tackles_stats.get("interceptions", 0)),
                        "duels_total": parse_int(duels_stats.get("total", 0)),
                        "duels_won": parse_int(duels_stats.get("won", 0)),
                        "dribbles_attempts": parse_int(dribbles_stats.get("attempts", 0)),
                        "dribbles_success": parse_int(dribbles_stats.get("success", 0)),
                        "dribbles_past": parse_int(dribbles_stats.get("past", 0)),
                        "fouls_drawn": parse_int(fouls_stats.get("drawn", 0)),
                        "fouls_committed": parse_int(fouls_stats.get("committed", 0)),
                        "yellow_cards": parse_int(cards_stats.get("yellow", 0)),
                        "red_cards": parse_int(cards_stats.get("red", 0)),
                        "penalties_won": parse_int(penalty_stats.get("won", 0)),
                        "penalties_committed": parse_int(penalty_stats.get("committed", 0)),
                        "penalties_scored": parse_int(penalty_stats.get("scored", 0)),
                        "penalties_missed": parse_int(penalty_stats.get("missed", 0)),
                        "penalties_saved": parse_int(penalty_stats.get("saved", 0)),
                    }

                    # Garantir que o dicionário tenha todas as 36 chaves
                    assert len(processed_player) == 36, f"Dicionário com tamanho incorreto: {len(processed_player)}"

                    processed_players.append(processed_player)

                except Exception as e:
                    print(f"Erro ao processar jogador {player.get('id')}: {e}")
                    print(f"Dados recebidos: {player_info}")

        return processed_players
