from .stages.pre.stage import PreProcessingStage
from .stages.post.stage import PostProcessingStage
from .stages.enhance.stage import EnchanceStage
import pprint


def main():

    heritage_ids = [38746] #31061, 34145, 135025]
    pre_stage = PreProcessingStage()
    enhance_stage = EnchanceStage()
    post_stage = PostProcessingStage

    # retrieve data
    retrieved_documents_per_heritage_object = pre_stage.run(heritage_objects=heritage_ids)
    pprint.pprint(retrieved_documents_per_heritage_object, indent=2)

    # process data
    enchance_output = enhance_stage.run(heritage_objects=retrieved_documents_per_heritage_object)
    pprint.pprint(enchance_output, indent=2)

    post_stage.run(findings=enchance_output)


if __name__ == "__main__":
    main()
