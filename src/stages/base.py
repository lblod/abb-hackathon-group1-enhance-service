import abc

class Stage(abc.ABC):

    def __init__(self):
        pass


    @abc.abstractmethod
    def run(self, *args, **kwargs) -> None:
        """
        The actually function that does the heavy lifting for a given stage
        """