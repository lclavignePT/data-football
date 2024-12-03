import requests
from config.settings import URL_BASE, API_KEY, LOG_DIR
from utils.logger import log_message
from utils.api_rate_limiter import can_make_request, record_api_call

LOG_FILE = LOG_DIR / "odds.log"

class OddsAPI:
    BASE_URL = URL_BASE
    API_KEY = API_KEY

    @staticmethod
    def get_odds(fixture_id, bookmaker_id):
        """
        Busca odds para um fixture específico e um bookmaker específico.
        """
        if not can_make_request():
            log_message("WARNING", "Limite diário de chamadas atingido. Abortando.", log_file=LOG_FILE, to_console=True)
            return None

        url = f"{OddsAPI.BASE_URL}/odds"
        headers = {"x-rapidapi-key": OddsAPI.API_KEY}
        params = {
            "fixture": fixture_id,
            "bookmaker": bookmaker_id
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Lança erro para códigos HTTP 4xx/5xx
            record_api_call()  # Registra a chamada
            log_message("INFO", f"Odds retornadas para fixture_id {fixture_id} e bookmaker_id {bookmaker_id}.", log_file=LOG_FILE)
            return response.json()
        except requests.exceptions.RequestException as e:
            log_message("ERROR", f"Erro na API para fixture_id {fixture_id}, bookmaker_id {bookmaker_id}: {e}", log_file=LOG_FILE, to_console=True)
            return None
