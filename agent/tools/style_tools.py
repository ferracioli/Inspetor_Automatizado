"""
Ferramenta para análise de estilo e legibilidade do código Python usando Pylint.
"""
import subprocess
import tempfile

class StyleAnalyzer:
    def analyze_code(self, code, filename="temp.py"):
        """Executa análise de estilo usando Pylint."""
        with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as temp:
            temp.write(code)
            temp_filename = temp.name
        try:
            result = subprocess.run(
                ['pylint', temp_filename, '--output-format=json'],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return {"status": "ok", "issues": []}
            else:
                import json
                output = json.loads(result.stdout) if result.stdout else []
                return {"status": "issues_found", "issues": output}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            import os
            os.unlink(temp_filename)
