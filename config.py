# Defina variáveis de configuração, como a chave da API OpenAI, caminho do repositório, intervalo de monitoramento
"""
Configurações globais do agente de validação de código.
"""
import os

# API_KEY = os.getenv("API_KEY", "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")
API_KEY = os.getenv("API_KEY", "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")
REPO_PATH = os.getenv("REPO_PATH", "../teste")
INTERVAL = int(os.getenv("INTERVAL", 300))
