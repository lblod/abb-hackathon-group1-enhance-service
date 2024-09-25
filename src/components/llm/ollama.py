from .base import LLM

from ollama import Client
import os


class OllamaLLM(LLM):
    def __init__(self):
        super().__init__()
        self.llm_client = Client(host=os.getenv("OLLAMA_HOST", "http://hackathon-ai-1.s.redhost.be:11434/"))

    def __call__(self, messages: list[dict[str, str]]) -> str:
        return self.llm_client.chat(model=self.MODEL, messages=messages)["message"]["content"]