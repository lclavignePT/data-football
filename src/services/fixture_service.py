class FixtureService:
    @staticmethod
    def process_fixtures(data):
        """
        Processa e valida os dados de fixtures recebidos da API.
        """
        processed_fixtures = []
        for fixture in data.get("response", []):
            processed_fixtures.append({
                "fixture_id": fixture["fixture"]["id"],
                "league_id": fixture["league"]["id"],
                "season": fixture["league"]["season"],
                "date": fixture["fixture"]["date"],
                "timestamp": fixture["fixture"]["timestamp"],
                "venue_id": fixture["fixture"].get("venue", {}).get("id"),
                "referee": fixture["fixture"].get("referee"),
                "home_team_id": fixture["teams"]["home"]["id"],
                "away_team_id": fixture["teams"]["away"]["id"],
                "home_goals": fixture["goals"]["home"],
                "away_goals": fixture["goals"]["away"],
                "halftime_home_goals": fixture["score"]["halftime"]["home"],
                "halftime_away_goals": fixture["score"]["halftime"]["away"]
            })
        return processed_fixtures
