"""
An interface for an ORM used in clingraph
"""
from abc import ABCMeta, abstractmethod

class ClingraphORM():
    """
    An interface for an ORM used in clingraph
    """
    __metaclass__ = ABCMeta

    def __init__(self, prefix: str = ""):
        """
        Creates an ORM that will serve as a database for the facts

        Args:
            prefix (str): The prefix to all predicate names
        """
        self.prefix = prefix

    @abstractmethod
    def add_fact_string(self, program):
        """
        Adds a string containing facts to the database

        Args:
            program (str): A string consisting of only facts, divided by a '.'
        """
        return NotImplementedError

    @abstractmethod
    def add_fact_file(self, file):
        """
        Adds a file containing facts to the database

        Args:
            file (str): The path to the file
        """
        return NotImplementedError

    @abstractmethod
    def add_clingo_model(self, model):
        """
        Adds a clingo model to the database

        Args:
            model (clingo.Model): A model returned by clingo
        """
        return NotImplementedError

    @abstractmethod
    def get_all_graphs(self):
        """
        Gets a list if the identifiers for all the graphs
        """
        return NotImplementedError

    @abstractmethod
    def parent_graph(self, graph_id):
        """
        Gets the parent graph for a given graph_id.
        Returns None if there is not such supertype

        Args:
            graph_id: Identifier of the subgraph
        """
        return NotImplementedError

    @abstractmethod
    def get_graph_global_element_attr(self, element_type, graph_id):
        """
        Gets the attributes for a global element: graph_nodes or graph_edges.
        Returns a dictionary where the keys are attribute name and values are
        attribute values.

        Args:
            element_type (str): The element type: 'edge' or 'node'
            graph_id: Identifier of the graph
        """
        return NotImplementedError

    @abstractmethod
    def get_graph_elements(self, element_type, graph_id):
        """
        Gets the list of elements for a graph

        Args:
            element_type (str): The element type: 'edge' or 'node'
            graph_id: Identifier of the graph
        """
        return NotImplementedError

    @abstractmethod
    def get_element_attr(self, element_type, element_id):
        """
        Gets the attributes a specific element
        Returns a dictionary where the keys are attribute name and values are
        attribute values.

        Args:
            element_type (str): The element type: 'graph', 'edge' or 'node'
            element_id: Identifier of the element
        """
        return NotImplementedError
