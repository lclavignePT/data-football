import sys
from pathlib import Path

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from api.update_fixtures import UpdateFixturesAPI
from services.update_fixtures_service import UpdateFixtureService
from db.helpers import update_fixture_processed_status
from db.insert import (
    insert_fixture,
    insert_fixture_events,
    insert_team_statistics,
    insert_start_xi,
    insert_substitutes,
    insert_player_statistics,
)
from utils.logger import log_message
from config.settings import LOG_DIR

LOG_FILE = LOG_DIR / "data/logs/update_fixtures.log"

class UpdateFixtureController:
    @staticmethod
    def update_fixture(fixture_id):
        """
        Orquestra o fluxo de atualização para um fixture específico.
        """
        try:
            log_message("INFO", f"Atualizando dados para fixture_id: {fixture_id}.", log_file=LOG_FILE)

            # Etapa 1: Buscar dados da API
            fixture_data = UpdateFixturesAPI.get_fixture_details(fixture_id)
            if not fixture_data:
                log_message("WARNING", f"Nenhum dado retornado para fixture_id: {fixture_id}.", log_file=LOG_FILE, to_console=True)
                return

            # Etapa 2: Processar os dados
            processed_data = UpdateFixtureService.process_fixture_data(fixture_data)

            # Etapa 3: Inserir os dados nas tabelas correspondentes
            insert_fixture(processed_data["fixtures"])
            insert_fixture_events(processed_data["events"])
            insert_team_statistics(processed_data["team_statistics"])
            insert_start_xi(processed_data["lineups"]["start_xi"])
            insert_substitutes(processed_data["lineups"]["substitutes"])
            insert_player_statistics(processed_data["player_statistics"])

            # Etapa 4: Atualizar o status para 'processed = 1'
            update_fixture_processed_status(fixture_id)

            log_message("INFO", f"Atualização concluída para fixture_id: {fixture_id}.", log_file=LOG_FILE)
        except Exception as e:
            log_message("ERROR", f"Erro ao atualizar fixture_id: {fixture_id}: {e}", log_file=LOG_FILE, to_console=True)
            raise
