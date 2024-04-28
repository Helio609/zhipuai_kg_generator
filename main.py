import logging
import os

from rich.logging import RichHandler

from args import Parser
from generator import Generator
from neo4j_driver import Neo4jDriver
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
logging.getLogger("neo4j").setLevel(level="ERROR")
logging.getLogger("neo4j.io").setLevel(level="ERROR")
logging.getLogger("neo4j.pool").setLevel(level="ERROR")


def main():
    args = Parser.parse()

    content: str | None = None
    if args.input.split(".")[-1] == "pdf":
        content = convert_pdf_to_text(args.input)
    else:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()

    driver: Neo4jDriver | None = None
    if args.neo4j:
        driver = Neo4jDriver(
            os.getenv("NEO4J_URI"),
            os.getenv("NEO4J_USERNAME"),
            os.getenv("NEO4J_PASSWORD"),
        )

    generator = Generator(model=args.model, main_language=args.language)
    knowledge_graph = generator.generate(
        content,
        args.output,
        args.window,
        parallel=args.parallel,
        split=args.split,
        update=args.update,
    )

    if args.neo4j:
        driver.insert_knowledge_graph(knowledge_graph)
        driver.close()


if __name__ == "__main__":
    main()
