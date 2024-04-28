import threading
from typing import List

from graphviz import Digraph
from langchain_core.pydantic_v1 import BaseModel, Field

mutex = threading.Lock()


class Node(BaseModel):
    label: str = Field(..., description="Label for the node")
    type: str = Field(..., description="Type of the node")


class Edge(BaseModel):
    # WARING: Notice that this is "from_", not "from"
    from_: str = Field(..., alias="from", description="Origin Node label")
    to: str = Field(..., description="Destination node label")
    relationship: str = Field(..., description="Type of relationship between the nodes")


class KnowledgeGraph(BaseModel):
    """Generate a knowledge graph with entities and relationships."""

    nodes: List[Node] = Field(..., description="List of nodes in the knowledge graph")
    edges: List[Edge] = Field(..., description="List of edges in the knowledge graph")

    def render(self, output_filename: str, format="png"):
        dot = Digraph(comment="Knowledge Graph", format=format, encoding="utf-8")

        for node in self.nodes:
            # dot.node(node.id, f"{node.label} ({node.type})")
            dot.node(node.label, node.label, fontname="Microsoft Yahei")

        for edge in self.edges:
            dot.edge(
                edge.from_, edge.to, label=edge.relationship, fontname="Microsoft Yahei"
            )

        # Support Chinese
        dot.graph_attr["charset"] = "utf-8"
        dot.attr("graph", fontname="Microsoft Yahei")
        dot.attr("node", fontname="Microsoft Yahei")
        dot.attr("edge", fontname="Microsoft Yahei")

        mutex.acquire()
        dot.render(output_filename, view=False)
        mutex.release()


import os
import unittest


class TestKnowledgeGraph(unittest.TestCase):

    def test_create_knowledge_graph(self):
        knowledge_graph = KnowledgeGraph(nodes=[], edges=[])

        knowledge_graph.render("test")

        self.assertTrue(os.path.exists("test.png"))

        os.remove("test")
        os.remove("test.png")


if __name__ == "__main__":
    unittest.main()
