from argparse import ArgumentParser

from pipelines.pipeline import Pipeline


def main():
    pipeline = Pipeline()
    parser = ArgumentParser(prog="fake-news-detection")
    parser.add_argument(
        "-e",
        "--explore",
        action="store_true",
        help="return data exploration",
    )
    arguments = parser.parse_args()
    if not arguments.explore:
        print(
            "× Please use flags, you may want to read the help message. Use: uv run main.py -h"
        )

    if arguments.explore:
        pipeline.data_exploration()

if __name__ == "__main__":
    main()
