# TODO: Ajustar para incluir funcao log_message
import sqlite3
import time
from config.settings import DB_PATH

def get_unprocessed_fixture_ids(db_path=DB_PATH):
    """
    Retorna uma lista de fixture_ids com timestamp menor que o atual e que ainda não foram processados (processed = 0).
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # Obter o timestamp atual
        current_timestamp = int(time.time())

        cursor.execute("""
            SELECT fixture_id FROM fixtures_id_processed
            WHERE timestamp < ? AND processed = 0
        """, (current_timestamp,))

        fixture_ids = [row[0] for row in cursor.fetchall()]
        return fixture_ids
    except Exception as e:
        raise RuntimeError(f"Erro ao buscar fixture_ids não processados: {e}")
    finally:
        connection.close()

def update_fixture_processed_status(fixture_id, db_path=DB_PATH):
    """
    Atualiza o status de um fixture para processed = 1 na tabela fixtures_id_processed.
    """
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE fixtures_id_processed
            SET processed = 1
            WHERE fixture_id = ?
        """, (fixture_id,))

        connection.commit()
    except Exception as e:
        raise RuntimeError(f"Erro ao atualizar o status do fixture_id {fixture_id}: {e}")
    finally:
        connection.close()

def get_coach_ids_from_fixtures(db_path=DB_PATH):
    """
    Executa a consulta SQL para obter os coach_id únicos
    das tabelas fixture_startXI e fixture_substitutes.

    :param db_path: Caminho para o arquivo do banco de dados SQLite.
    :return: Lista de coach_id distintos.
    """
    query = """
    WITH
    -- União de todos os CoachId das duas tabelas
    all_coach_ids AS (
        SELECT coach_id FROM fixture_startXI
        UNION ALL
        SELECT coach_id FROM fixture_substitutes
    )
    -- Seleciona apenas os CoachId distintos no conjunto All, excluindo valores NULL
    SELECT DISTINCT coach_id
    FROM all_coach_ids
    WHERE coach_id IS NOT NULL;
    """
    try:
        # Usar context manager para conexão com SQLite
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Executar a consulta e recuperar os resultados
            cursor.execute(query)
            coach_ids = [row[0] for row in cursor.fetchall()]

        # Adicionar log para validação
        print(f"Coach IDs encontrados: {len(coach_ids)}")  # DEBUG: Log para verificar retorno
        return coach_ids
    except sqlite3.Error as e:
        raise Exception(f"Erro ao consultar os coach_id: {e}")
