# Integre o LLM como "cérebro" do agente
# Desenvolva prompts especializados para análise de código
# Crie a lógica de tomada de decisão baseada nos resultados

from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory

class CodeValidatorAgent:
    def __init__(self, api_key):
        self.llm = OpenAI(temperature=0, api_key=api_key)
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
        self.tools = [
            Tool(
                name="SecurityAnalyzer",
                func=self.security_analyzer.analyze_code,
                description="Analisa o código em busca de vulnerabilidades de segurança"
            ),
            Tool(
                name="StyleAnalyzer", 
                func=self.style_analyzer.analyze_code,
                description="Verifica o estilo e legibilidade do código"
            ),
            Tool(
                name="DocumentationAnalyzer",
                func=self.doc_analyzer.analyze_documentation,
                description="Avalia a qualidade e completude da documentação do código"
            )
        ]
        
        self.agent = initialize_agent(
            self.tools, 
            self.llm, 
            agent="conversational-react-description", 
            memory=self.memory,
            verbose=True
        )
        
    def validate_code(self, code, context=None):
        """Valida o código usando o agente e retorna os resultados."""
        prompt = self._build_validation_prompt(code, context)
        return self.agent.run(prompt)
    
    def _build_validation_prompt(self, code, context):
        """Constrói o prompt para o agente com instruções específicas."""
        return f"""
        Analise o seguinte código Python e identifique problemas relacionados a:
        1. Segurança
        2. Estilo e legibilidade
        3. Documentação e manutenibilidade
        
        Utilize as ferramentas disponíveis para fazer uma análise profunda.
        Depois, forneça um relatório detalhado com problemas encontrados e sugestões
        de melhorias concretas.
        
        Contexto adicional: {context or 'Nenhum contexto adicional fornecido.'}
        
        Código:
        ```
        {code}
        ```
        """
