from ..base import Stage

from .utils import insert_heritage_objects


class PostProcessingStage(Stage):

    def __init__(self):
        super().__init__()


    def run(self, *args, **kwargs) -> None:

        findings = kwargs.get("findings")
        insert_heritage_objects(findings)



