from agent.tools.security_tools import SecurityAnalyzer
from agent.tools.style_tools import StyleAnalyzer
from agent.tools.documentation_tools import DocumentationAnalyzer

from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory

from agent.llms.openrouter_llm import OpenRouterLLM

class CodeValidatorAgent:
    def __init__(self):
        self.llm = OpenRouterLLM()
        self.memory = ConversationBufferMemory(memory_key="chat_history")
        
        self.security_analyzer = SecurityAnalyzer()
        self.style_analyzer = StyleAnalyzer()
        self.doc_analyzer = DocumentationAnalyzer()

        self.tools = []
        # self.tools = [
        #     Tool(
        #         name="SecurityAnalyzer",
        #         func=self.security_analyzer.analyze_code,
        #         description="Analisa o código em busca de vulnerabilidades de segurança"
        #     ),
        #     Tool(
        #         name="StyleAnalyzer", 
        #         func=self.style_analyzer.analyze_code,
        #         description="Verifica o estilo e legibilidade do código"
        #     ),
        #     Tool(
        #         name="DocumentationAnalyzer",
        #         func=self.doc_analyzer.analyze_documentation,
        #         description="Avalia a qualidade e completude da documentação do código"
        #     )
        # ]
        
        self.agent = initialize_agent(
            self.tools, 
            self.llm, 
            agent="conversational-react-description", 
            memory=self.memory,
            verbose=True
        )

    def validate_code(self, code, context=None, callback=None, file_path=None):
        prompt = self._build_validation_prompt(code, context)
        print("validate_code da code_validator.py")

        # Se não passou callback, executa normalmente (sem streaming)
        if callback is None:
            return self.agent.run(prompt)

        # Streaming com callback
        # Supondo que self.llm tem método `stream` que gera tokens
        full_response = ""
        for token in self.llm.stream(prompt):
            full_response += token

        # print("full_response")
        # print(full_response)
        callback(full_response, file_path)

        return full_response

        
    def _build_validation_prompt(self, code, context):
        return f"""
        Analise o seguinte codigo Python e identifique problemas relacionados a:
        1. Seguranca
        2. Estilo e legibilidade
        3. Documentacao e manutenibilidade
        
        Utilize as ferramentas disponiveis para fazer uma analise profunda.
        Depois, forneca um relatorio detalhado com problemas encontrados e sugestoes
        de melhorias concretas, mas não amplie o código para operacoes que ele ainda
        nao faz no momento.
        
        Contexto adicional: {context or 'Nenhum contexto adicional fornecido.'}
        
        Codigo:
        ```
        {code}
        ```
        """