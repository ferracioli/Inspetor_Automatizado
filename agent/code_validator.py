from agent.tools.security_tools import SecurityAnalyzer
from agent.tools.style_tools import StyleAnalyzer
from agent.tools.documentation_tools import DocumentationAnalyzer

from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from agent.llms.openrouter_llm import OpenRouterLLM

class CodeValidatorAgent:
    def __init__(self):
        self.llm = OpenRouterLLM()
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        self.security_analyzer = SecurityAnalyzer()
        self.style_analyzer = StyleAnalyzer()
        self.doc_analyzer = DocumentationAnalyzer()

        # Definir ferramentas
        self.tools = [
            Tool(
                name="StyleAnalyzer", 
                func=self.style_analyzer.analyze_code,
                description="give the full filepath as input, returns the output of the pylint code analysis"
            )
        ]
        
        # Criar prompt para o agente
        self.prompt = ChatPromptTemplate.from_messages([
                    ('system', """
                You are an agent capable of calling tools. These are the tools available: {tools}

                Follow these **strict** formatting rules:

                1. **Always** begin your response with `Thought:`.
                2. **If you are calling a tool**, include **only** these three lines, and **nothing else**:
                    Thought: [Very short reasoning sentence]\nAction: [ToolName, must be one of the options {tool_names}]\nAction Input: [tool_input]
                    — and **stop** your response there. The system will execute the tool and then return `Observation:` in a new turn.
                3. **If you are giving the final answer to the user**, include **only** these lines:
                    Thought: Final Answer\nFinal Answer: [your response to the user]
                4. **Never** mix `Action` and `Final Answer` in the same turn.
                5. **Never** manually show `Observation:`.

                **Valid Examples**  
                - *Tool Call*:
                    'Thought: I need to validate the code style\nAction: StyleAnalyzer\nAction Input: /path/to/file.py'

                - *Final Answer*:
                    'Thought: Final Answer\nFinal Answer: your answer...'

                **Invalid Examples**  
                - Mixing tool call and final answer  
                - Manually inserting `Observation:`  
                - Any extra text outside the formats above
                """),
                    ('system', 'Here is a set of tools and their outputs: {agent_scratchpad}'),
                    ('user', '{input}')
        ])




        
        # Criar agente usando ReAct (mais compatível com diversos modelos)
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )

        # Configurar executor
        self.executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            max_iterations=3,
            handle_parsing_errors=True,
            return_intermediate_steps = True
        )

    def _build_validation_prompt(self, code, context):
        return f"""
        Analyze the following Python code and identify issues related to style:{code}
        
        Additional context: {context or 'No additional context provided.'}
        
        Provide a detailed analysis using the available tools and synthesize the results into a report listing the issues found and concrete suggestions for improvement.
        After that, please provide the corrected code with comments explaining it.
        """


    def validate_code(self, code, context=None):
        prompt = self._build_validation_prompt(code, context)
        return self.executor.invoke({"input": prompt})
