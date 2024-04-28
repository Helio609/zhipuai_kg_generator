from logging import getLogger

from neo4j import GraphDatabase

from models import Edge, Node


class Neo4jDriver:
    def __init__(self, uri, user, password):
        self.__logger = getLogger(__name__)
        self.__uri = uri
        self.__user = user
        self.__password = password
        self.__driver = None
        self.__connect()

    def __connect(self):
        try:
            self.__driver = GraphDatabase.driver(
                self.__uri, auth=(self.__user, self.__password)
            )
        except Exception as e:
            self.__logger.fatal(f"Failed to connect to neo4j database: {e}")
            exit(1)

    def close(self):
        if self.__driver:
            self.__driver.close()

    def create_node(self, node: Node):
        with self.__driver.session() as session:
            session.run(
                f"CREATE (n:Node:`{node.type}` {{ label: $label }})", label=node.label
            )

    def create_edge(self, edge: Edge):
        with self.__driver.session() as session:
            session.run(
                f"MATCH (a:Node:`{edge.from_}`), (b:Node:`{edge.to}`) "
                + f"CREATE (a)-[:`{edge.relationship}`]->(b)"
            )

    def insert_knowledge_graph(self, knowledge_graph):
        try:
            with self.__driver.session() as session:
                session.write_transaction(
                    self.__insert_knowledge_graph, knowledge_graph
                )
        except Exception as e:
            self.__logger.fatal(f"Failed to create knowledge graph in neo4j {e}")
            exit(1)

    def __insert_knowledge_graph(self, tx, knowledge_graph):
        for node in knowledge_graph.nodes:
            tx.run(
                f"CREATE (n:Node:`{node.type}` {{ label: $label }})", label=node.label
            )

        for edge in knowledge_graph.edges:
            tx.run(
                f"MATCH (a:Node {{label:'{edge.from_}'}}), (b:Node {{label:'{edge.to}'}}) "
                + f"CREATE (a)-[:{edge.relationship}]->(b)"
            )
