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
logger = logging.getLogger(__name__)


def load_content(filename: str) -> str:
    content: str | None = None
    if not os.path.exists(filename):
        logger.fatal("File does not exists")
        exit(1)

    if filename.split(".")[-1] == "pdf":
        content = convert_pdf_to_text(filename)
    else:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

    return content


def main():
    args = Parser.parse()

    content = load_content(args.input)

    driver: Neo4jDriver | None = None
    if args.neo4j:
        driver = Neo4jDriver(
            os.getenv("NEO4J_URI"),
            os.getenv("NEO4J_USERNAME"),
            os.getenv("NEO4J_PASSWORD"),
        )
        logger.info("Created Neo4j client")

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
        logger.info("Start insert knowledge graph")
        driver.insert_knowledge_graph(knowledge_graph)
        driver.close()


if __name__ == "__main__":
    main()
