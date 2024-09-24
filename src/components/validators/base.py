import abc


class Validator(abc.ABC):

    def __init__(self):
        pass

    @abc.abstractmethod
    def validate(self, text: str) -> tuple[str, bool]:
        pass
