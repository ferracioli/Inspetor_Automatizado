# Defina variáveis de configuração, como a chave da API OpenAI, caminho do repositório, intervalo de monitoramento
"""
Configurações globais do agente de validação de código.
"""
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
REPO_PATH = os.getenv("REPO_PATH", "./")
INTERVAL = int(os.getenv("INTERVAL", 300))
