from pathlib import Path
import sys

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from api.coachs import CoachAPI
from services.coach_service import CoachService
from db.insert import insert_coach
from db.helpers import get_coach_ids_from_fixtures
from utils.logger import log_message

def ingest_coachs():
    """
    Orquestra o fluxo para ingestão de dados de coachs.
    """
    try:
        # Buscar os coach_ids únicos das tabelas fixture_startXI e fixture_substitutes
        coach_ids = get_coach_ids_from_fixtures()
        if not coach_ids:
            log_message("INFO", "Nenhum coach_id encontrado nas tabelas.", "data/logs/coach_ingest.log", to_console=True)
            return

        for coach_id in coach_ids:
            # Buscar dados da API
            coach_data = CoachAPI.get_coach(coach_id)

            if not coach_data:
                log_message("WARNING", f"Dados não encontrados para coach_id {coach_id}. Pulando...", "data/logs/coach_ingest.log", to_console=True)
                continue

            # Processar os dados
            try:
                processed_data = CoachService.process_coach(coach_data)
            except ValueError as ve:
                log_message("WARNING", f"{ve}. Coach_id: {coach_id}. Pulando...", "data/logs/coach_ingest.log", to_console=True)
                continue

            # Inserir os dados processados no banco
            insert_coach(processed_data)
            log_message("INFO", f"Coach {processed_data['name']} inserido com sucesso.", "data/logs/coach_ingest.log", to_console=True)
    except Exception as e:
        log_message("ERROR", f"Erro no fluxo de ingestão de coachs: {e}", "data/logs/coach_ingest.log", to_console=True)
