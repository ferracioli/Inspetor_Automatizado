from typing import ClassVar
from langchain.llms.base import LLM
from config import API_KEY
import requests
import json

class OpenRouterLLM(LLM):
    api_url: ClassVar[str] = 'https://openrouter.ai/api/v1/chat/completions'
    # api_url: ClassVar[str] = 'https://openrouter.ai/api/v1'

    # model: str = "llama-2-70b-chat"
    model: str = "deepseek/deepseek-v3-base:free"
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
        print("URL:", self.api_url)
        print("Headers:", headers)
        print("JSON:", json.dumps(json_data, indent=2))
        response = requests.post(self.api_url, headers=headers, json=json_data, timeout=30)
        response.raise_for_status()
        print(">>")
        print(response)
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)
        data = response.json()
        return data["choices"][0]["message"]["content"]

    @property
    def _identifying_params(self):
        return {"model": self.model}

    @property
    def _llm_type(self) -> str:
        return "openrouter"