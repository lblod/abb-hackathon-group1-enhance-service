import abc

class LLM(abc.ABC):
    MODEL = "llama3.1"

    def __init__(self) -> None:
        self.llm_client = None


    @abc.abstractmethod
    def __call__(self, messages: list[dict[str, str]]) -> str:
        pass