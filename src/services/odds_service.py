from utils.logger import log_message
from config.settings import LOG_DIR
from datetime import datetime

class OddsService:
    LOG_FILE = LOG_DIR / "odds_service.log"

    @staticmethod
    def _format_timestamp(timestamp_str):
        """
        Converte uma string de data e hora (ISO 8601) para o formato TIMESTAMP do SQLite.
        """
        try:
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            log_message("ERROR", f"Erro ao formatar timestamp: {e}", log_file=OddsService.LOG_FILE)
            return None

    @staticmethod
    def process_odds_data(odds_data):
        """
        Processa o JSON retornado pela API para extrair os mercados e odds relevantes,
        combinando mercados relacionados em um único dicionário por fixture_id.
        """
        try:
            response = odds_data.get("response", [])
            if not response:
                log_message("WARNING", "Nenhuma resposta encontrada no JSON.", log_file=OddsService.LOG_FILE)
                return []

            odds_result = []
            for item in response:
                fixture_id = item["fixture"]["id"]
                updated_at = item.get("update")
                if not updated_at:
                    log_message(
                        "WARNING",
                        f"Campo 'update' ausente no JSON para fixture_id {fixture_id}. Dados: {item}",
                        log_file=OddsService.LOG_FILE
                    )
                    continue
                updated_at = OddsService._format_timestamp(updated_at)

                bookmakers = item.get("bookmakers", [])
                combined_odds = OddsService._initialize_combined_odds(fixture_id, updated_at)

                for bookmaker in bookmakers:
                    if bookmaker["name"] == "Betfair":
                        for bet in bookmaker.get("bets", []):
                            if bet["name"] == "Match Winner":
                                combined_odds.update(OddsService._process_match_winner(bet))
                            elif bet["name"] == "Goals Over/Under":
                                combined_odds.update(OddsService._process_goals_over_under(bet))

                odds_result.append(combined_odds)

            log_message("INFO", f"{len(odds_result)} odds processadas.", log_file=OddsService.LOG_FILE)
            return odds_result
        except Exception as e:
            log_message("ERROR", f"Erro ao processar odds: {e}", log_file=OddsService.LOG_FILE)
            return []

    @staticmethod
    def _initialize_combined_odds(fixture_id, updated_at):
        """
        Inicializa o dicionário de odds combinadas para um fixture_id específico.
        """
        return {
            "fixture_id": fixture_id,
            "home_win": None,
            "draw": None,
            "away_win": None,
            "over_0_5": None, "under_0_5": None,
            "over_1_5": None, "under_1_5": None,
            "over_2_5": None, "under_2_5": None,
            "over_3_5": None, "under_3_5": None,
            "over_4_5": None, "under_4_5": None,
            "over_5_5": None, "under_5_5": None,
            "over_6_5": None, "under_6_5": None,
            "updated_at": updated_at,
        }

    @staticmethod
    def _process_match_winner(bet):
        """
        Processa o mercado 'Match Winner' e retorna as odds home_win, draw e away_win.
        """
        odds = {"home_win": None, "draw": None, "away_win": None}
        for value in bet.get("values", []):
            if value["value"] == "Home":
                odds["home_win"] = float(value["odd"])
            elif value["value"] == "Draw":
                odds["draw"] = float(value["odd"])
            elif value["value"] == "Away":
                odds["away_win"] = float(value["odd"])
        return odds

    @staticmethod
    def _process_goals_over_under(bet):
        """
        Processa o mercado 'Goals Over/Under' e retorna as odds para vários limites.
        """
        odds = {
            "over_0_5": None, "under_0_5": None,
            "over_1_5": None, "under_1_5": None,
            "over_2_5": None, "under_2_5": None,
            "over_3_5": None, "under_3_5": None,
            "over_4_5": None, "under_4_5": None,
            "over_5_5": None, "under_5_5": None,
            "over_6_5": None, "under_6_5": None,
        }
        for value in bet.get("values", []):
            if "Over" in value["value"]:
                key = "over_" + value["value"].split(" ")[1].replace(".", "_")
            elif "Under" in value["value"]:
                key = "under_" + value["value"].split(" ")[1].replace(".", "_")
            else:
                continue
            odds[key] = float(value["odd"])
        return odds
