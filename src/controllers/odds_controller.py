import sys
from pathlib import Path
import sqlite3

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from api.odds import OddsAPI
from db.helpers import get_fixture_ids_after_date
from services.odds_service import OddsService
from utils.logger import log_message
from config.settings import LOG_DIR, DB_PATH
from db.insert import insert_odds

LOG_FILE = LOG_DIR / "odds_controller.log"

class OddsController:
    @staticmethod
    def ingest_odds(bookmaker_id=3):
        """
        Atualiza odds no banco de dados para fixtures com timestamp maior que a data inicial.
        """
        log_message("INFO", "Iniciando atualização de odds.", log_file=LOG_FILE)

        fixture_ids = get_fixture_ids_after_date()
        if not fixture_ids:
            log_message("INFO", "Nenhum fixture encontrado para atualizar.", log_file=LOG_FILE)
            return {"message": "Nenhum fixture encontrado."}

        fixtures_with_odds = 0

        for fixture_id in fixture_ids:
            try:
                odds_data = OddsAPI.get_odds(fixture_id, bookmaker_id)
                if not odds_data or not odds_data.get("response"):
                    log_message("WARNING", f"Odds não encontradas para fixture_id {fixture_id}.", log_file=LOG_FILE)
                    continue

                processed_odds = OddsService.process_odds_data(odds_data)
                if not processed_odds:
                    log_message(
                        "WARNING",
                        f"Odds não processadas para fixture_id {fixture_id}. JSON recebido: {odds_data}",
                        log_file=LOG_FILE
                    )
                    continue

                insert_odds(DB_PATH, fixture_id, processed_odds)
                fixtures_with_odds += 1
                log_message("INFO", f"Odds inseridas para fixture_id {fixture_id}.", log_file=LOG_FILE)

            except sqlite3.Error as e:
                log_message("ERROR", f"Erro no banco para fixture_id {fixture_id}: {e}", log_file=LOG_FILE)
            except Exception as e:
                log_message("ERROR", f"Erro inesperado: {e}", log_file=LOG_FILE)

        log_message("INFO", f"Atualização concluída: {fixtures_with_odds} fixtures processados.", log_file=LOG_FILE)
        return {"fixtures_with_odds": fixtures_with_odds}
