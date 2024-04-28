import logging

from rich.logging import RichHandler

from args import Parser
from generator import Generator
from pdf import convert_pdf_to_text

FORMAT = "[%(name)s] %(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)
logging.getLogger("httpx").setLevel(level="ERROR")
logging.getLogger("httpcore.http11").setLevel(level="ERROR")
logging.getLogger("httpcore.proxy").setLevel(level="ERROR")
logging.getLogger("httpcore.connection").setLevel(level="ERROR")
logging.getLogger("urllib3.connectionpool").setLevel(level="ERROR")
logging.getLogger("graphviz.saving").setLevel(level="ERROR")
logging.getLogger("graphviz.backend.execute").setLevel(level="ERROR")


def main():
    args = Parser.parse()

    content: str | None = None
    if args.input.split(".")[-1] == "pdf":
        content = convert_pdf_to_text(args.input)
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()

    generator = Generator(model=args.model, main_language=args.language)
    generator.generate(
        content,
        args.output,
        args.window,
        parallel=args.parallel,
        split=args.split,
        update=args.update,
    )


if __name__ == "__main__":
    main()
