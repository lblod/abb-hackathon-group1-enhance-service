import os

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ...components.data.datasource import DataSource


from ...components.llm import OllamaLLM
from ...components.retry_prompter import OutputRetryParser
from ...components.validators import JsonValidator
from ..base import Stage
from .utils import get_prompt


class EnchanceStage(Stage):

    def __init__(self):
        super().__init__()
        self.llm = OllamaLLM()
        self.prompter = OutputRetryParser(self.llm)
        self.validator = JsonValidator()

    def run(self, *args: Any, **kwargs: Any) -> Any:
        rules = []

        for item in kwargs.get("heritage_objects", []):
            #TODO: iterate over content and save "page" also in the rule?
            #TODO: designation object id in rule or just added later in post?

            _id = item["id"]
            for data_obj in item["object"]:
                data_obj: DataSource
                extracted_rules = self.__extract(data_obj.content)
                print(extracted_rules)

                for extracted_rule in extracted_rules:

                    rule = extracted_rule.get("rule", "")
                    if len(rule) <= 3:
                        print("EMPTY RULE:", extracted_rule)
                        continue

                    rules.append(dict(source = _id, source_type=data_obj.filetype, rule=rule))

        return rules

    def __extract(self, legal_content):
        messages = get_prompt(legal_content)
        response = self.prompter(messages, self.validator)
        return response

    """[
        {
            "rule": "<The rule that can be interpretated seperately>",
            "legality": "The legality of this rule. Must be either "legaal", "illegaal", "toestemming verreist" or "undefined"",
            "source": "<source document>",
            "source_type": "management plan, decision or law", #TODO: check the RDD spec for the correct urls
            "page": "<Page number>" #If we iterate over indiviual pages
        }
    ]"""
