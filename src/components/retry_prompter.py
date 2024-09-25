from typing import Any
from .llm.base import LLM
from .validators import Validator


class OutputRetryParser:
    DEFAULT_INSTRUCTION = "While attempting to parse the output, the following error was received ```{error}```"

    def __init__(self, llm: LLM, max_retries: int = 5) -> None:
        self.llm = llm
        self.max_retries = max_retries

    def __call__(
            self,
            conversation: list[dict[str, str]],
            output_validator: Validator,
            error_instruction: str = None,
        ) -> Any:

        error_instruction = error_instruction or self.DEFAULT_INSTRUCTION

        i: int = 0
        while i < self.max_retries:
            llm_output = self.llm(conversation)
            validation_output, succes = output_validator.validate(llm_output)

            if succes:
                return validation_output

            conversation += [
                dict(role="assistant", content=llm_output),
                dict(role="user", content=error_instruction.format(error=validation_output))
            ]

        raise ValueError("Failed to parse into requested format")
