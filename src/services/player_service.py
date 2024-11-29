import orjson
import gzip
import sqlite3

json_path = "data/profiles.json.gz"
db_path = "data/db/database.sqlite"

def get_player_ids_from_db(db_path=db_path):
    """
    Executa a consulta SQL para obter os player_id distintos do banco de dados.
    """
    query = """
    WITH
    all_player_ids AS (
        SELECT player_id FROM fixture_events
        UNION ALL
        SELECT player_id FROM fixture_player_statistics
        UNION ALL
        SELECT player_id FROM fixture_startXI
        UNION ALL
        SELECT player_id FROM fixture_substitutes
    )
    SELECT DISTINCT player_id
    FROM all_player_ids
    WHERE player_id IS NOT NULL;
    """
    try:
        # Conectar ao banco e executar a consulta
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        player_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return set(player_ids)  # Retornar como conjunto para facilitar filtros
    except sqlite3.Error as e:
        raise Exception(f"Erro ao consultar o banco de dados: {e}")


import orjson
import gzip
import sqlite3

def load_players_from_json(json_path=json_path, db_path=db_path):
    """
    Carrega jogadores do arquivo JSON compactado no formato GZIP,
    filtra pelo conjunto de player_id retornado da consulta SQL,
    e retorna uma lista de dicionários com player_id e name.
    """
    try:
        # Obter player_id únicos do banco
        valid_player_ids = get_player_ids_from_db(db_path)

        # Abrir o arquivo GZIP e carregar o JSON com ORJSON
        with gzip.open(json_path, 'rb') as file:
            data = orjson.loads(file.read())
        
        # Verificar se o JSON contém o campo "response"
        if "response" not in data or not isinstance(data["response"], list):
            raise Exception("O JSON não contém o campo 'response' ou ele não é uma lista.")

        # Acessar a lista de jogadores no campo "response"
        all_players = data["response"]

        # Filtrar jogadores pelo conjunto de player_id do banco
        players = []
        for item in all_players:
            # Garantir que a estrutura esperada existe
            if "player" in item and isinstance(item["player"], dict):
                player_data = item["player"]
                if player_data.get("id") in valid_player_ids and "name" in player_data:
                    players.append({
                        "player_id": player_data["id"],
                        "name": player_data["name"]
                    })

        return players
    except FileNotFoundError:
        raise Exception(f"O arquivo {json_path} não foi encontrado.")
    except (orjson.JSONDecodeError, gzip.BadGzipFile):
        raise Exception(f"Erro ao processar o arquivo JSON compactado {json_path}.")
    except Exception as e:
        raise Exception(f"Erro inesperado: {e}")
