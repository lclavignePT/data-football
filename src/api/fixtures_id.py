import requests
from config.settings import URL_BASE, API_KEY, LOG_DIR
from utils.logger import log_message
from utils.api_rate_limiter import can_make_request, record_api_call

LOG_FILE=LOG_DIR / "fixtures_id.log"

class FixtureIDAPI:
    BASE_URL = URL_BASE
    API_KEY = API_KEY

    @staticmethod
    def get_fixtures_ids(league_id, season):
        """
        Busca fixtures de uma liga e temporada específicas para popular fixtures_id_processed.
        """
        if not can_make_request():
            log_message("WARNING", "Limite diário de chamadas atingido. Abortando.", log_file=LOG_FILE, to_console=True)
            return None

        url = f"{FixtureIDAPI.BASE_URL}/fixtures"
        headers = {"x-rapidapi-key": FixtureIDAPI.API_KEY}
        params = {"league": league_id, "season": season}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Lança erro para códigos HTTP 4xx/5xx
            record_api_call()  # Registra a chamada
            return response.json()
        except requests.exceptions.RequestException as e:
            log_message("ERROR", f"Erro na API: {e}", log_file=LOG_FILE, to_console=True)
            return None
