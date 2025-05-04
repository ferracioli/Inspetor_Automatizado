from typing import ClassVar
from langchain.llms.base import LLM
from config import API_KEY
import requests
import json

class OpenRouterLLM(LLM):
    api_url: ClassVar[str] = 'https://openrouter.ai/api/v1/chat/completions'
    # api_url: ClassVar[str] = 'https://openrouter.ai/api/v1'

    model: str = "huggingfaceh4/zephyr-7b-beta:free"
    # model: str = "microsoft/phi-4-reasoning-plus:free"
    temperature: float = 0.0
    headers: dict = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

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
    
    def stream(self, prompt: str):
        print("Entrando na stream")
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
        }

        with requests.post(self.api_url, headers=self.headers, json=payload, stream=True) as response:
            print("Response:\n")
            print(response.text)
            response.raise_for_status()
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                line = line.strip()
                if line.startswith("data: "):
                    data = line[len("data: "):]
                    if data == "[DONE]":
                        break
                    try:
                        data_obj = json.loads(data)
                        content = data_obj["choices"][0]["delta"].get("content")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue

    @property
    def _identifying_params(self):
        return {"model": self.model}

    @property
    def _llm_type(self) -> str:
        return "openrouter"