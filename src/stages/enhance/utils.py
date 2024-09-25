def get_prompt(legal_content):
    return [
    {
        "role": "user",
        "content": f"""The following text is an excerpt of a governmental decision.
        {legal_content}
        
        Extract and all the rules regarding actions/changes to monuments that are legal, require permission or are illegal from the text above.
        Every rule should be interpretable seperately!
        
        Use the following format:
        
        [
            {{
                "rule": <The rule that can be interpretated seperately>,
                "legality": The legality of this rule. Must be either "legaal", "illegaal", "toestemming verreist" or "undefined",
            }}, ...
        ]
        
        Don't use list items (like a), 1.,  -)
        The json vlaues in your output should be entirely in Dutch.
        The json keys should remain english
        """
    },
    {
        "role": "assistant",
        "content": """Hier zijn de onafhankelijke regels:"""
    }
]