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
    parser.add_argument(
        "-i",
        "--insert",
        action="store_true",
        help="process data and insert everything into chromadb",
    )
    parser.add_argument(
        "-r",
        "--run",
        action="store_true",
        help="allows user to provide text for a news article to check whether or not it is reliable information",
    )
    arguments = parser.parse_args()
    if not arguments.explore and not arguments.insert and not arguments.run:
        print(
            "× Please use flags, you may want to read the help message. Use: uv run main.py -h"
        )

    if arguments.explore:
        pipeline.data_exploration()
    if arguments.insert:
        pipeline.chroma_insertion()
    if arguments.run:
        pipeline.process_user_input()


if __name__ == "__main__":
    main()
