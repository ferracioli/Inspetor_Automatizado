import requests
from langchain.schema import LLMResult, Generation
from langchain.llms.base import LLM
from typing import ClassVar

class FreeLLM(LLM):
    """Wrapper simples para uma API gratuita de LLM via HTTP GET."""

    # api_url: str = 'https://openrouter.ai/api/v1/chat/completions'
    api_url: ClassVar[str] = 'https://openrouter.ai/api/v1/chat/completions'

    def _call(self, prompt: str, stop=None) -> str:
        try:
            response = requests.get(
                self.api_url,
                params={"query": prompt},
                headers={"Accept": "application/json"},
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            return f"Erro na chamada da API: {e}"

    @property
    def _identifying_params(self):
        return {"api_url": self.api_url}

    @property
    def _llm_type(self) -> str:
        return "free-llm"
