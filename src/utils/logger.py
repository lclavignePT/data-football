import time
import os

def log_message(level, message, log_file, to_console=False):
    """
    Registra mensagens no log e no console, conforme necessário.

    Args:
        level (str): O nível do log (INFO, ERROR, WARNING, etc.).
        message (str): A mensagem a ser registrada.
        log_file (str): O caminho completo do arquivo de log.
        to_console (bool): Se True, exibe a mensagem no console.
    """
    # Garante que o diretório do log exista
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {level} - {message}\n"
    with open(log_file, "a") as log:
        log.write(log_entry)
    if to_console and level in {"INFO", "ERROR"}:
        print(f"{level} - {message}")
