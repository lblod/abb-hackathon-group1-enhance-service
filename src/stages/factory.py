from .base import Stage


def get_stage(stage:str) -> Stage:

    match stage.lower():
        case "ingestion":
            return NotImplementedError()
        case "enhancing":
            return NotImplementedError()
        case "writing":
            return NotImplementedError()
