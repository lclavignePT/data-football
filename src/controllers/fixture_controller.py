import sys
from pathlib import Path

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from config.settings import LEAGUES_SEASONS
from api.fixtures import FixtureAPI
from services.fixture_service import FixtureService
from db.insert import insert_fixtures
from db.queries import get_stored_fixture_ids
from utils.logger import log_message
import yaml

def ingest_fixtures(config_file=LEAGUES_SEASONS):
    """
    Orquestra o fluxo de coleta e inserção de fixtures, evitando duplicatas.
    """
    try:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)

        for league in config["leagues"]:
            league_id = league["id"]
            for season in league["seasons"]:
                # Verificar quais fixtures já estão no banco
                stored_fixture_ids = get_stored_fixture_ids(league_id, season)
                
                log_message("INFO", f"Buscando fixtures para Liga {league['name']} Temporada {season}.", "data/logs/fixture_ingest.log", to_console=True)

                # Buscar dados da API
                data = FixtureAPI.get_fixtures(league_id, season)
                if not data:
                    log_message("WARNING", f"Sem dados para Liga {league['name']} Temporada {season}.", "data/logs/fixture_ingest.log", to_console=True)
                    continue

                # Filtrar fixtures novas
                fixtures_to_insert = [
                    fixture for fixture in FixtureService.process_fixtures(data)
                    if fixture["fixture_id"] not in stored_fixture_ids
                ]

                if fixtures_to_insert:
                    insert_fixtures(fixtures_to_insert)
                else:
                    log_message("INFO", f"Nenhuma nova fixture para inserir na Liga {league['name']} Temporada {season}.", "data/logs/fixture_ingest.log", to_console=True)
    except Exception as e:
        log_message("ERROR", f"Erro no fluxo de ingestão: {e}", "data/logs/fixture_ingest.log", to_console=True)