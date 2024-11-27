import sys
from pathlib import Path

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from controllers.fixture_controller import ingest_fixtures
from controllers.team_controller import ingest_teams
from utils.logger import log_message
from config.settings import LOG_DIR

LOG_FILE = LOG_DIR / "main.log"

if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    try:
        log_message("INFO", "Iniciando fluxo de ingestão de dados.", log_file=LOG_FILE, to_console=True)
        ingest_fixtures()
        ingest_teams()
        log_message("INFO", "Fluxo concluído com sucesso!", log_file=LOG_FILE, to_console=True)
    except Exception as e:
        log_message("ERROR", f"Erro inesperado: {e}", log_file=LOG_FILE, to_console=True)
