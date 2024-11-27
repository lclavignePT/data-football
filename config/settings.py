import os
from dotenv import load_dotenv
from pathlib import Path

# Definir a raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carregar o arquivo .env da raiz
load_dotenv(BASE_DIR / ".env")

# Configurações
API_KEY = os.getenv("API_KEY")
URL_BASE = os.getenv("URL_BASE", "https://v3.football.api-sports.io/")
DB_PATH = Path(os.getenv("DB_PATH", "data/db/database.sqlite"))
LOG_DIR = Path(os.getenv("LOG_PATH", "data/logs"))
REQUEST_COUNT_FILE = BASE_DIR / "data/logs/request_count.yaml"

# Criar diretórios padrão, se não existirem
os.makedirs(LOG_DIR, exist_ok=True)