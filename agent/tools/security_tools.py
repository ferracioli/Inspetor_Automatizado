# Integre ferramentas básicas de análise de código Python
# Configure wrappers para Bandit (segurança), Pylint (estilo) e Docstring-coverage

import subprocess
import json
import tempfile

class SecurityAnalyzer:
    def analyze_code(self, code, filename="temp.py"):
        """Executa análise de segurança usando Bandit."""
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as temp:
            temp.write(code)
            temp_filename = temp.name
            
        try:
            # Execute Bandit com saída JSON
            result = subprocess.run(
                ['bandit', '-f', 'json', temp_filename],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {"status": "secure", "issues": []}
            else:
                output = json.loads(result.stdout)
                return {
                    "status": "issues_found",
                    "issues": output.get("results", [])
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            # Limpar arquivo temporário
            import os
            os.unlink(temp_filename)
