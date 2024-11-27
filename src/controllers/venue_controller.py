import sys
from pathlib import Path

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from api.venues import VenueAPI
from services.venue_service import VenueService
from db.insert import insert_venue
from db.queries import get_venue_ids_from_fixtures
from utils.logger import log_message

def ingest_venues():
    """
    Orquestra o fluxo para ingestão de dados de venues.
    """
    try:
        # Buscar os venue_ids únicos da tabela fixtures
        venue_ids = get_venue_ids_from_fixtures()
        if not venue_ids:
            log_message("INFO", "Nenhum venue_id encontrado nas fixtures.", "data/logs/venue_ingest.log", to_console=True)
            return

        for venue_id in venue_ids:
            # Buscar dados da API
            venue_data = VenueAPI.get_venue(venue_id)

            if not venue_data:
                log_message("WARNING", f"Dados não encontrados para venue_id {venue_id}. Pulando...", "data/logs/venue_ingest.log", to_console=True)
                continue

            # Processar os dados
            try:
                processed_data = VenueService.process_venue(venue_data)
            except ValueError as ve:
                log_message("WARNING", f"{ve}. Venue_id: {venue_id}. Pulando...", "data/logs/venue_ingest.log", to_console=True)
                continue

            # Inserir os dados processados no banco
            insert_venue(processed_data)
            log_message("INFO", f"Venue {processed_data['name']} inserido com sucesso.", "data/logs/venue_ingest.log", to_console=True)
    except Exception as e:
        log_message("ERROR", f"Erro no fluxo de ingestão de venues: {e}", "data/logs/venue_ingest.log", to_console=True)
