import sys
from pathlib import Path

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from config.settings import LEAGUES_SEASONS, LOG_DIR
from api.fixtures_id import FixtureIDAPI
from services.fixtures_id_service import FixtureIDService
from db.insert import insert_fixtures_ids
from utils.logger import log_message
import yaml

LOG_FILE = LOG_DIR / "fixtures_id_ingest.log"

class FixtureIDController:
    @staticmethod
    def ingest_fixtures_ids(config_file=LEAGUES_SEASONS):
        """
        Orquestra o fluxo de coleta e inserção de dados na tabela fixtures_id_processed.
        """
        try:
            # Carregar configurações de ligas e temporadas do arquivo YAML
            with open(config_file, "r") as file:
                config = yaml.safe_load(file)

            for league in config["leagues"]:
                league_id = league["id"]
                league_name = league["name"]

                for season in league["seasons"]:
                    # Verificar se a temporada já foi processada
                    if season.get("processed", False):
                        log_message("INFO", f"Temporada {season['year']} da Liga {league_name} já processada. Ignorando.", log_file=LOG_FILE)
                        continue

                    season_year = season["year"]
                    log_message("INFO", f"Buscando fixtures para Liga {league_name} Temporada {season_year}.", log_file=LOG_FILE)

                    # Buscar dados da API
                    data = FixtureIDAPI.get_fixtures_ids(league_id, season_year)
                    if not data:
                        log_message("WARNING", f"Sem dados para Liga {league_name} Temporada {season_year}.", log_file=LOG_FILE, to_console=True)
                        continue

                    # Processar dados
                    processed_ids = FixtureIDService.process_fixtures_ids(data)

                    # Inserir dados no banco
                    if processed_ids:
                        insert_fixtures_ids(processed_ids)
                        log_message("INFO", f"Fixtures inseridas com sucesso para Liga {league_name} Temporada {season_year}.", log_file=LOG_FILE)
                        # Marcar a temporada como processada
                        season["processed"] = True
                    else:
                        log_message("INFO", f"Nenhuma nova fixture para inserir na Liga {league_name} Temporada {season_year}.", log_file=LOG_FILE, to_console=True)

            # Atualizar o arquivo YAML com as mudanças
            with open(config_file, "w") as file:
                yaml.safe_dump(config, file)

        except Exception as e:
            log_message("ERROR", f"Erro no fluxo de ingestão: {e}", log_file=LOG_FILE, to_console=True)
