class VenueService:
    @staticmethod
    def process_venue(data):
        """
        Processa os dados de um venue retornado pela API.
        """
        if not data or "response" not in data or not data["response"]:
            raise ValueError("Nenhum dado encontrado na resposta da API para o venue.")

        venue_data = data["response"][0]  # Primeiro elemento da lista
        return {
            "venue_id": venue_data["id"],
            "name": venue_data["name"],
            "capacity": venue_data.get("capacity"),
            "city": venue_data.get("city"),
            "surface": venue_data.get("surface"),
        }
