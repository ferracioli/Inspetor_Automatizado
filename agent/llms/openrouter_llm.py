from typing import ClassVar
from langchain.llms.base import LLM
from config import API_KEY
import requests

class OpenRouterLLM(LLM):
    api_url: ClassVar[str] = 'https://openrouter.ai/api/v1/chat/completions'

    model: str = "llama-2-70b-chat"
    temperature: float = 0.0

    def _call(self, prompt: str, stop=None) -> str:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        json_data = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature,
            "max_tokens": 1000
        }
        response = requests.post(self.api_url, headers=headers, json=json_data, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]

    @property
    def _identifying_params(self):
        return {"model": self.model}

    @property
    def _llm_type(self) -> str:
        return "openrouter"


# import requests
# from langchain.schema import LLMResult, Generation
# from langchain.llms.base import LLM
# from typing import ClassVar
# from config import API_KEY

# class OpenRouterLLM(LLM):
#     # api_url = "https://openrouter.ai/api/v1/chat/completions"
#     api_url: ClassVar[str] = 'https://openrouter.ai/api/v1/chat/completions'
#     model: str = "llama-2-70b-chat"
#     temperature: float = 0.0
    
#     # def __init__(self, api_key: str, model: str = "llama-2-70b-chat", temperature: float = 0.0):
#     def __init__(self, model: str = "llama-2-70b-chat", temperature: float = 0.0):
#         # self.api_key = API_KEY
        
#         self.model = model
#         self.temperature = temperature
    
#     def _call(self, prompt: str, stop=None) -> str:
#         headers = {
#             # "Authorization": f"Bearer {self.API_KEY}",
#             "Authorization": f"Bearer {API_KEY}",
#             "Content-Type": "application/json"
#         }
#         json_data = {
#             "model": self.model,
#             "messages": [{"role": "user", "content": prompt}],
#             "temperature": self.temperature,
#             "max_tokens": 1000
#         }
#         response = requests.post(self.api_url, headers=headers, json=json_data, timeout=30)
#         response.raise_for_status()
#         data = response.json()
#         return data["choices"][0]["message"]["content"]
    
#     @property
#     def _identifying_params(self):
#         return {"model": self.model}
    
#     @property
#     def _llm_type(self) -> str:
#         return "openrouter"
