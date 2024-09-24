from .base import Validator
import json


class JsonValidator(Validator):

    def validate(self, text: str) -> tuple[str, bool]:
        try:
            parsed = json.loads(text)
            return parsed, True
        except Exception as e:
            return f"Error in json syntax: {e}", True
