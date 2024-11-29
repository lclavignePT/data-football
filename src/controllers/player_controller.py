import sys
from pathlib import Path

# Adicionar a raiz do projeto e o diretório `src` ao sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
SRC_DIR = BASE_DIR / "src"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))  # Para importar `config.settings`

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))  # Para importar `utils.file_utils`

from services.player_service import load_players_from_json
import sqlite3

json_path = "data/profiles.json.gz"
db_path = "data/db/database.sqlite"

def ingest_players(json_path=json_path, db_path=db_path):
    """
    Insere jogadores únicos no banco de dados a partir do JSON fornecido.
    """
    try:
        # Carregar os jogadores do JSON
        players = load_players_from_json(json_path)

        # Conectar ao banco SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Inserir jogadores no banco
        for player in players:
            try:
                cursor.execute(
                    "INSERT OR IGNORE INTO players (player_id, name) VALUES (?, ?)",
                    (player["player_id"], player["name"])
                )
            except sqlite3.IntegrityError as e:
                print(f"Erro ao inserir jogador {player['player_id']}: {e}")

        # Commit e fechar conexão
        conn.commit()
        conn.close()
        print(f"Jogadores inseridos com sucesso a partir do arquivo {json_path}!")
    except Exception as e:
        print(f"Erro: {e}")
