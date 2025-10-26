# src/app/settings_manager.py

import json
import sys
import os

CONFIG_FILE_PATH = "config.json"

def load_settings():
    """
    Carrega as configurações do config.json.
    Assume que o arquivo existe e está no formato JSON correto.
    """
    try:
        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as f:
            settings = json.load(f)
            return settings
            
    except FileNotFoundError:
        print(f"--- ERRO CRÍTICO ---")
        print(f"O arquivo '{CONFIG_FILE_PATH}' não foi encontrado.")
        print(f"Por favor, certifique-se que o 'config.json' está na mesma pasta que 'run.py'.")
        print(f"Caminho atual: {os.getcwd()}")
        sys.exit(1) # Encerra a aplicação
        
    except json.JSONDecodeError:
        print(f"--- ERRO CRÍTICO ---")
        print(f"O arquivo '{CONFIG_FILE_PATH}' contém um erro de sintaxe (JSON inválido).")
        print("Por favor, verifique o arquivo por vírgulas faltantes, chaves, etc.")
        sys.exit(1) # Encerra a aplicação
        
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar as configurações: {e}")
        sys.exit(1) # Encerra a aplicação