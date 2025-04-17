"""
Ferramenta para análise de documentação de código Python (docstrings).
"""
import ast

class DocumentationAnalyzer:
    def analyze_documentation(self, code):
        """Avalia a presença de docstrings em funções e classes."""
        try:
            tree = ast.parse(code)
            missing = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if ast.get_docstring(node) is None:
                        missing.append({
                            "type": type(node).__name__,
                            "name": getattr(node, 'name', None),
                            "line": node.lineno
                        })
            return {"missing_docstrings": missing, "total": len(missing)}
        except Exception as e:
            return {"error": str(e)}
