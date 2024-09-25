from .base import Validator
import json


class JsonValidator(Validator):

    def validate(self, text: str) -> tuple[str, bool]:
        print("validating:", text)
        try:
            parsed = json.loads(text)
            return parsed, True
        except Exception as e:
            print("FAILED")
            return f"Error in json syntax: {e}", False
