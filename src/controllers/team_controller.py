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
from api.teams import TeamAPI
from services.team_service import TeamService
from db.insert import insert_teams
from db.queries import get_stored_team_ids
from utils.logger import log_message
import yaml

def ingest_teams(config_file=LEAGUES_SEASONS):
    """
    Orquestra o fluxo de coleta e inserção de times, evitando duplicatas.
    """
    try:
        with open(config_file, "r") as file:
            config = yaml.safe_load(file)

        for league in config["leagues"]:
            league_id = league["id"]
            league_name = league["name"]

            for season in league["seasons"]:
                # Obter o ano da temporada e verificar se está processada
                season_year = season["year"]

                log_message("INFO", f"Buscando times para Liga {league_name} Temporada {season_year}.", 
                            "data/logs/team_ingest.log", to_console=True)

                # Verificar quais teams já estão no banco
                stored_team_ids = get_stored_team_ids(league_id)

                # Buscar dados da API
                data = TeamAPI.get_teams(league_id, season_year)
                if not data:
                    log_message("WARNING", f"Sem dados para Liga {league_name} Temporada {season_year}.", 
                                "data/logs/team_ingest.log", to_console=True)
                    continue

                # Filtrar times novos
                teams_to_insert = [
                    team for team in TeamService.process_teams(data)
                    if team["team_id"] not in stored_team_ids
                ]

                if teams_to_insert:
                    insert_teams(teams_to_insert)
                    log_message("INFO", f"Times inseridos com sucesso na Liga {league_name} Temporada {season_year}.", 
                                "data/logs/team_ingest.log", to_console=True)
                else:
                    log_message("INFO", f"Nenhum novo time para inserir na Liga {league_name} Temporada {season_year}.", 
                                "data/logs/team_ingest.log", to_console=True)
    except Exception as e:
        log_message("ERROR", f"Erro no fluxo de ingestão de times: {e}", 
                    "data/logs/team_ingest.log", to_console=True)