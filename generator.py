import os
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger

from langchain.output_parsers import PydanticOutputParser
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import PromptTemplate

from models import KnowledgeGraph
from splitter import split_sentence

TEMPLATE = """请使用给定格式以及主要语言{language}创建知识图谱:\n{format_instructions}\n确保所有的节点和边是与下文相关的:\n```\n{topic}\n```"""


class Generator:
    def __init__(self, model: str, main_language: str) -> None:
        self._logger = getLogger(__name__)

        self._parser = PydanticOutputParser(pydantic_object=KnowledgeGraph)
        self._prompt = PromptTemplate(
            template=TEMPLATE,
            input_variables=["topic"],
            partial_variables={
                "format_instructions": self._parser.get_format_instructions(),
                "language": main_language,
            },
        )
        self._chat = ChatZhipuAI(model=model, api_key=os.getenv("ZHIPUAI_API_KEY"))
        self._chain = self._prompt | self._chat | self._parser

        self._logger.info(f"Init the Generator with model: {model}")

    def generate(
        self,
        content: str,
        output_filename: str,
        window: int,
        parallel: int = 1,
        split: bool = True,
        update: bool = True,
        retry=3,
    ):
        sentences = []
        if split:
            sentences = split_sentence(content)
        else:
            sentences.append(content)

        knowledge_graph = KnowledgeGraph(
            nodes=[],
            edges=[],
        )

        def process(i, text: str, retry: int):
            retry_ = retry
            while retry_:
                try:
                    # self._logger.debug(f"input: {text}")

                    output = self._chain.invoke({"topic": text})

                    # self._logger.debug(f"output: {output}")

                    knowledge_graph.nodes += output.nodes
                    knowledge_graph.edges += output.edges

                    self._logger.info(
                        f"Processed {i + 1} part of contents, node: {len(knowledge_graph.nodes)}, edge: {len(knowledge_graph.edges)}"
                    )

                    if update:
                        knowledge_graph.render(output_filename)
                    break
                except OutputParserException:
                    retry_ -= 1
                    self._logger.warning(
                        f"Failed to generate the {i + 1} part of knowledge graph due to output format, retry..."
                    )
            else:
                self._logger.warn(f"Skip the {i + 1} part due to too many errors")

        self._logger.info(f"Total need to process: {len(sentences)}")
        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = [
                executor.submit(process, i, "\n".join(sentences[i : i + window]), retry)
                for i in range(len(sentences) - window + 1)
            ]

        knowledge_graph.render(output_filename)

        return knowledge_graph
