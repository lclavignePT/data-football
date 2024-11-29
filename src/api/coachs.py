import requests
from pathlib import Path
import sys

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from config.settings import URL_BASE, API_KEY
from utils.logger import log_message
from utils.api_rate_limiter import can_make_request, record_api_call


class CoachAPI:
    BASE_URL = URL_BASE
    API_KEY = API_KEY

    @staticmethod
    def get_coach(coach_id):
        """
        Busca informações detalhadas de um coach pelo ID.
        """
        if not can_make_request():
            log_message("WARNING", "Limite diário de chamadas atingido. Abortando.", "data/logs/api_requests.log", to_console=True)
            return None

        url = f"{CoachAPI.BASE_URL}/coachs"
        headers = {"x-rapidapi-key": CoachAPI.API_KEY}
        params = {"id": coach_id}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Lança erro para códigos HTTP 4xx/5xx
            record_api_call()  # Registra a chamada

            data = response.json()
            if "response" not in data or not data["response"]:
                log_message("WARNING", f"Dados não encontrados para coach_id {coach_id}.", "data/logs/api_requests.log", to_console=True)
                return None

            return data
        except requests.exceptions.RequestException as e:
            log_message("ERROR", f"Erro na API: {e}", "data/logs/api_requests.log", to_console=True)
            return None
