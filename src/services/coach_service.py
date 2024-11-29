class CoachService:
    @staticmethod
    def process_coach(data):
        """
        Processa os dados de um coach retornado pela API.
        """
        if not data or "response" not in data or not data["response"]:
            raise ValueError("Nenhum dado encontrado na resposta da API para o coach.")

        coach_data = data["response"][0]  # Primeiro elemento da lista
        return {
            "coach_id": coach_data["id"],
            "name": coach_data["name"]
        }
