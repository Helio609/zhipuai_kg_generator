import argparse
from logging import getLogger

from dotenv import load_dotenv


class Parser:
    def parse():
        load_dotenv()

        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-i", "--input", help="Input file path, support pure text file and pdf"
        )
        parser.add_argument(
            "-o",
            "--output",
            help="Output graphviz file name",
            default="knowledge_graph",
        )
        parser.add_argument(
            "-s",
            "--split",
            help="Split content, default to true",
            action="store_true",
        )
        parser.add_argument(
            "-w",
            "--window",
            help="A sliding window to control the number of sentences to be processed at a time",
            type=int,
            default=0,
        )
        parser.add_argument(
            "-m", "--model", help="The model used to generate the KG", default="glm-4"
        )
        parser.add_argument(
            "-p",
            "--parallel",
            help="The max worker in thread pool",
            type=int,
            default=1,
        )
        parser.add_argument("-l", "--language", default="中文")
        parser.add_argument(
            "-u",
            "--update",
            help="Render in real time when nodes or edges changed",
            action="store_true",
        )
        args = parser.parse_args()

        Parser._validate(args)

        return args

    def _validate(args):
        logger = getLogger(__name__)
        if not args.input:
            logger.fatal("Please enter the filename via --input <FILENAME>")
            exit(1)
