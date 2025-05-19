from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (
    AIMessage,
    FunctionMessage,
    HumanMessage,
    SystemMessage,
    ToolMessage,
)
from langchain_core.outputs import ChatGeneration, ChatGenerationChunk, ChatResult
from pydantic import Field

import requests
from config import API_KEY

def process_agent_scratchpad(agent_scratchpad: str):
    """
    Processa um agent_scratchpad e retorna duas mensagens do LangChain:
    1. AIMessage: contém a parte do pensamento e ação do agente
    2. SystemMessage: contém a observação/resposta do sistema
    
    Args:
        agent_scratchpad (str): O texto completo do scratchpad
        
    Returns:
        tuple: (AIMessage, SystemMessage)
    """
    # Dividir o scratchpad pela palavra "Observation:"
    parts = agent_scratchpad.split("Observation:", 1)
    
    # Conteúdo para o AIMessage (pensamento e ação)
    ai_content = parts[0].strip()
    
    # A parte da observação pode ter um "Thought:" no final que deve ser removido
    observation_part = parts[1]
    
    # Verificar se há um "Thought:" no final para removê-lo
    if "Thought:" in observation_part:
        observation_content = observation_part.split("Thought:", 1)[0].strip()
    else:
        observation_content = observation_part.strip()
    
    # Criar as mensagens
    ai_message = AIMessage(content=ai_content)
    system_message = SystemMessage(content=observation_content)
    
    return ai_message, system_message


class OpenRouterLLM(BaseChatModel):
    # def __init__(self, **data):
        # api_url = Field(default="https://openrouter.ai/api/v1/chat/completions")
        # model = Field(default="deepseek/deepseek-chat-v3-0324:free")
        # temperature = Field(default=0.01)
        # max_tokens = Field(default=1000)
        # self.headers={
        #     "Authorization": f"Bearer {API_KEY}",
        #     "Content-Type": "application/json"
        # }

    def _generate(self, langchain_messages, stop = None, run_manager = None, **kwargs):
        
        openrouter_messages = []
        for message in langchain_messages:
            
            # print('mensagem------')
            # print(message.text())
            # print('fim da mensagem------')

            if 'Here is a set of tools and their outputs:' in message.text() and len(message.text())>42:
                ai_msg, system_msg = process_agent_scratchpad(message.text()[42:])
                openrouter_messages.append({"role": "AI", "content": ai_msg.text()})
                openrouter_messages.append({"role": "system", "content":system_msg.text()})
                continue

            if 'Here is a set of tools and their outputs:' in message.text():
                continue
            
            if isinstance(message, SystemMessage):
                role = "system"
                content = message.text()
            elif isinstance(message, HumanMessage):
                role = "user"
                content = message.text()
            elif isinstance(message, AIMessage):
                role = "assistant"
                content = message.text()
            elif isinstance(message, ToolMessage):
                role = "tool"  # Use "function" if required by OpenRouter
                content = f"Tool Result: {message.content}"
            else:
                print(f'tipo de mensagem não indentificada: {type(message)}')
                continue
        
            openrouter_messages.append({"role": role, "content": content})


        # print(f'mensagens a enviar ao servidor:{openrouter_messages}')
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
            },
            json={
                "model": "deepseek/deepseek-r1:free",
                "messages": openrouter_messages,
                "temperature": 0.20,
                "max_tokens": 5000,
                **kwargs
            },
            timeout=30
        ).json()
            
        # print(response)
        text = response["choices"][0]["message"]["content"]
        # print('-------------------resposta do modelo-------------------')
        # print(text)
        # print('--------------------------------------------------------')
        final_message = AIMessage(content = text)

        
        generation = ChatGeneration(message=final_message)
        return ChatResult(generations=[generation])

    async def _astream(self, prompt, stop = None, run_manager = None, **kwargs):
        # Implementação assíncrona (opcional)
        pass

    @property
    def _llm_type(self) -> str:
        return "openrouter"

    def get_num_tokens(self, text: str) -> int:
        # Implemente se necessário para token counting
        return len(text.split())





