import os

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
        
    def __call__(self, *args: os.Any, **kwds: os.Any) -> os.Any:
        rules = []
        
        for item in args:
            #TODO: iterate over content and save 'page' also in the rule?
            #TODO: designation object id in rule or just added later in post?
            extracted_rules = self.__extract(item.content)
            
            for extracted_rule in extracted_rules:
                extracted_rule["source"] = item.id
                extracted_rule["source_type"] = item.source_type
            
        return rules
    
    def __extract(self, legal_content):
        messages = get_prompt(legal_content)
        response = self.prompter(messages, self.validator)
        return response
    
    
    """[
        {
            'rule': '<The rule that can be interpretated seperately>',
            'legality': "The legality of this rule. Must be either 'legaal', 'illegaal', 'toestemming verreist' or 'undefined'",
            'source': '<source document>',
            'source_type': 'management plan, decision or law', #TODO: check the RDD spec for the correct urls
            'page': '<Page number>' #If we iterate over indiviual pages
        }
    ]"""