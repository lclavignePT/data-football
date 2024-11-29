import sys
from pathlib import Path

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from controllers.update_fixtures_controller import UpdateFixtureController
from utils.logger import log_message
from config.settings import LOG_DIR
from db.helpers import get_unprocessed_fixture_ids

LOG_FILE = LOG_DIR / "update.log"

if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True, exist_ok=True)

def run_update():

    try:
        log_message("INFO", "Iniciando atualização de fixtures detalhados.", log_file=LOG_FILE, to_console=True)

        # Buscar todos os fixture_ids não processados
        unprocessed_fixture_ids = get_unprocessed_fixture_ids()

        if not unprocessed_fixture_ids:
            log_message("INFO", "Nenhum fixture não processado encontrado.", log_file=LOG_FILE, to_console=True)
        else:
            for fixture_id in unprocessed_fixture_ids:
                UpdateFixtureController.update_fixture(fixture_id)

        log_message("INFO", "Atualização de fixtures detalhados concluída com sucesso!", log_file=LOG_FILE, to_console=True)
    except Exception as e:
        log_message("ERROR", f"Erro inesperado: {e}", log_file=LOG_FILE, to_console=True)

if __name__ == "__main__":
    run_update()