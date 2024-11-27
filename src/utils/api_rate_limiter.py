import yaml
import time
import datetime
import os
import sys
from pathlib import Path

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from src.utils.logger import log_message

REQUEST_COUNT_FILE = "data/logs/request_count.yaml"
LOG_FILE = "data/logs/api_requests.log"

def load_request_count(file_path=REQUEST_COUNT_FILE):
    """
    Carrega o contador de chamadas da API do arquivo YAML.
    """
    try:
        if not os.path.exists(file_path):
            reset_request_count(file_path)
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        log_message("ERROR", f"Erro ao carregar o contador: {e}", LOG_FILE, to_console=True)
        return None

def save_request_count(data, file_path=REQUEST_COUNT_FILE):
    """
    Salva o contador de chamadas da API no arquivo YAML.
    """
    try:
        with open(file_path, "w") as file:
            yaml.dump(data, file)
        log_message("INFO", f"Dados salvos com sucesso: {data}", LOG_FILE)
    except Exception as e:
        log_message("ERROR", f"Erro ao salvar o contador: {e}", LOG_FILE, to_console=True)

def reset_request_count(file_path=REQUEST_COUNT_FILE):
    """
    Reseta o contador de chamadas no arquivo YAML.
    """
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    data = {"api_calls": {"total": 0, "last_reset": today, "limit": 7000}}
    save_request_count(data, file_path)
    log_message("INFO", "Contador de chamadas resetado.", LOG_FILE)

def can_make_request(file_path=REQUEST_COUNT_FILE):
    """
    Verifica se é possível fazer uma nova chamada à API.
    """
    data = load_request_count(file_path)
    if not data:
        log_message("ERROR", "Não foi possível carregar o contador.", LOG_FILE)
        return False

    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")

    # Reseta o contador se for um novo dia
    if data["api_calls"]["last_reset"] != today:
        reset_request_count(file_path)
        data = load_request_count(file_path)

    if data["api_calls"]["total"] < data["api_calls"]["limit"]:
        return True
    else:
        log_message("WARNING", "Limite diário de chamadas à API atingido.", LOG_FILE)
        return False

def record_api_call(file_path=REQUEST_COUNT_FILE):
    """
    Registra uma nova chamada à API.
    """
    data = load_request_count(file_path)
    if data:
        data["api_calls"]["total"] += 1
        save_request_count(data, file_path)
        log_message("INFO", f"Chamada registrada. Total: {data['api_calls']['total']}", LOG_FILE)