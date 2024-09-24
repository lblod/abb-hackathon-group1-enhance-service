from .stages.factory import get_stage

from fire import fire


def main(stage, **kwargs) -> None:
    get_stage(stage).run(**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
