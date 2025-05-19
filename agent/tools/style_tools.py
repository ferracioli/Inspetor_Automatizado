"""
Ferramenta para análise de estilo e legibilidade do código Python usando Pylint.
"""
import subprocess
import json

class StyleAnalyzer:
    def analyze_code(self, filename):
        """Executa análise de estilo usando Pylint em um arquivo existente."""
        try:
            result = subprocess.run(
                ['pylint', filename, '--output-format=json'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0 or not result.stdout:
                return f"No issues found in file '{filename}'."

            issues = json.loads(result.stdout)
            if not issues:
                return f"No issues found in file '{filename}'."

            formatted_issues = "\n".join([
                f"- [{issue.get('type', 'unknown').upper()}] "
                f"Line {issue.get('line', '?')}: {issue.get('message', '')} "
                f"(ID: {issue.get('message-id', 'N/A')})"
                for issue in issues
            ])
            return f"Issues found in file '{filename}':\n{formatted_issues}"

        except Exception as e:
            return f"Error while analyzing '{filename}': {str(e)}"
