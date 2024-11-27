class TeamService:
    @staticmethod
    def process_teams(data):
        """
        Processa e valida os dados de times recebidos da API.
        """
        processed_teams = []
        for team in data.get("response", []):
            processed_teams.append({
                "team_id": team["team"]["id"],
                "name": team["team"]["name"],
                "country": team["team"]["country"],
                "founded": team["team"]["founded"],
                "venue_id": team["venue"].get("id")
            })
        return processed_teams
