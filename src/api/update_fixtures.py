import requests
from config.settings import URL_BASE, API_KEY, LOG_DIR
from utils.logger import log_message
from utils.api_rate_limiter import can_make_request, record_api_call

LOG_FILE=LOG_DIR / "update_fixtures.log"

class UpdateFixturesAPI:
    BASE_URL = URL_BASE
    API_KEY = API_KEY

    @staticmethod
    def get_fixture_details(fixture_id):
        """
        Busca os detalhes de um fixture específico pelo fixture_id.
        """
        if not can_make_request():
            log_message("WARNING", "Limite diário de chamadas atingido. Abortando.", log_file=LOG_FILE, to_console=True)
            return None

        url = f"{UpdateFixturesAPI.BASE_URL}/fixtures"
        headers = {"x-rapidapi-key": UpdateFixturesAPI.API_KEY}
        params = {"id": fixture_id}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Lança erro para códigos HTTP 4xx/5xx
            record_api_call()  # Registra a chamada
            return response.json()
        except requests.exceptions.RequestException as e:
            log_message("ERROR", f"Erro na API ao buscar fixture {fixture_id}: {e}", log_file=LOG_FILE, to_console=True)
            return None
