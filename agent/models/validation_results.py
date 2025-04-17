# Implemente a geração de relatórios de validação
# Desenvolva sugestões automáticas de correção
# Configure sistema para salvar resultados e histórico

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

@dataclass
class SecurityIssue:
    severity: str
    description: str
    line_number: int
    code: Optional[str] = None
    fix_suggestion: Optional[str] = None

@dataclass
class StyleIssue:
    type: str
    description: str
    line_number: int
    code: Optional[str] = None
    fix_suggestion: Optional[str] = None

@dataclass
class DocumentationIssue:
    type: str
    description: str
    affected_element: str
    fix_suggestion: Optional[str] = None

@dataclass
class ValidationResult:
    file_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    security_issues: List[SecurityIssue] = field(default_factory=list)
    style_issues: List[StyleIssue] = field(default_factory=list)
    documentation_issues: List[DocumentationIssue] = field(default_factory=list)
    security_score: float = 100.0
    style_score: float = 100.0
    documentation_score: float = 100.0
    overall_quality: float = 100.0
    summary: str = ""
    improvement_suggestions: List[str] = field(default_factory=list)
