# Implemente o ciclo completo (percepção > análise > ação)
# Desenvolva uma interface CLI básica para interação
# Adicione capacidade do agente iniciar verificações automaticamente

import os
import time
import argparse
from agent.code_validator import CodeValidatorAgent
from integrations.git_integrations import GitHandler

from config import OPENAI_API_KEY
from config import REPO_PATH

# def monitor_repository(repo_path, interval=300):
def monitor_repository(repo_path="./", interval=300):
    """Monitora um repositório periodicamente e valida novos arquivos."""

    print("Iniciando código")

    agent = CodeValidatorAgent(OPENAI_API_KEY)
    # git_handler = GitHandler(repo_path)
    git_handler = GitHandler(REPO_PATH)
    
    processed_files = set()
    
    print(f"Iniciando monitoramento do repositório: {repo_path}")
    print(f"O agente verificará novos arquivos a cada {interval} segundos")
    
    try:
        while True:
            print("\nVerificando novos arquivos Python...")
            python_files = git_handler.get_latest_python_files()
            
            new_files = [f for f in python_files if f not in processed_files]
            if new_files:
                print(f"Encontrados {len(new_files)} novos arquivos para validar")
                
                for file_path in new_files:
                    print(f"\nValidando: {file_path}")
                    code = git_handler.get_file_content(file_path)
                    
                    if code:
                        result = agent.validate_code(
                            code, 
                            context=f"Arquivo: {file_path}"
                        )
                        
                        # Aqui o agente toma a ação de salvar resultados
                        print(f"Resultado da validação para {file_path}:")
                        print(result)
                        
                        # Adiciona à lista de processados
                        processed_files.add(file_path)
                    else:
                        print(f"Não foi possível ler o arquivo: {file_path}")
            else:
                print("Nenhum novo arquivo para validar")
                
            print(f"Aguardando {interval} segundos até a próxima verificação...")
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agente de Validação de Código Python")
    # parser.add_argument("--repo", required=True, help="Caminho para o repositório Git")
    parser.add_argument("--repo", default="./", help="Caminho para o repositório Git")
    parser.add_argument("--interval", type=int, default=300, help="Intervalo de verificação em segundos")
    
    args = parser.parse_args()
    monitor_repository(args.repo, args.interval)
