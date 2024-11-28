class FixtureIDService:
    @staticmethod
    def process_fixtures_ids(data):
        """
        Processa e valida os dados de fixtures recebidos da API para a tabela fixtures_id_processed.
        """
        processed_ids = []
        for fixture in data.get("response", []):
            processed_ids.append({
                "fixture_id": fixture["fixture"]["id"],
                "timestamp": fixture["fixture"]["timestamp"]
            })
        return processed_ids
