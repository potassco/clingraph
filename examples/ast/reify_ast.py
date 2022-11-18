#!/usr/bin/env python3

from clingo.ast import AST, ASTSequence, Location, Position, parse_files
from clingo.symbol import Symbol
from clorm import Predicate, IntegerField, ConstantField, StringField, combine_fields, refine_field, FactBase
from typing import Optional, Union
import sys

PREFIX = "ast_"

class Node(Predicate):
    id = IntegerField
    key = refine_field(ConstantField, ["type", "variant", "value", "level"])
    value = combine_fields([IntegerField, StringField])

    class Meta:
        name = PREFIX + "node"

class Edge(Predicate):
    id = (IntegerField, IntegerField)
    key = refine_field(ConstantField, ["key"])
    value = combine_fields([IntegerField, StringField])

    class Meta:
        name = PREFIX + "edge"

class ReifiedAST:
    def __init__(self):
        self.__node_count = 1
        self.__statement_count = 0
        self.__factbase = FactBase([
            Node(0, "type", "ASTSequence"),
            Node(0, "level", 0),
        ])

    def __str__(self):
        return self.__factbase.asp_str()

    def add_node(
        self,
        node: Union[AST, ASTSequence, Location, Symbol, int, str],
        parent_id: int = 0,
        parent_key: Optional[int] = None,
        level: int = 1
    ):
        # Create an identifier for the new node
        node_id = self.__node_count
        self.__node_count += 1

        # Derive the key, if necessary
        if parent_key is None:
            parent_key = self.__statement_count
            self.__statement_count +=1

        # Add the edge
        edge_id = (parent_id, node_id)
        self.__factbase.add(Edge(edge_id, "key", parent_key))

        # Add the node
        items = []

        if isinstance(node, AST):
            self.__factbase.add(Node(node_id, "type", "AST"))
            self.__factbase.add(Node(node_id, "level", level))
            self.__factbase.add(Node(node_id, "variant", node.ast_type.name))
            self.__factbase.add(Node(node_id, "value", str(node)))
            items = node.items()

        elif isinstance(node, ASTSequence):
            self.__factbase.add(Node(node_id, "type", "ASTSequence"))
            self.__factbase.add(Node(node_id, "level", level))
            items = enumerate(node)

        elif isinstance(node, Location):
            self.__factbase.add(Node(node_id, "type", "Location"))
            self.__factbase.add(Node(node_id, "level", level))
            items = [('begin', node.begin), ("end", node.end)]

        elif isinstance(node, Position):
            self.__factbase.add(Node(node_id, "type", "Position"))
            self.__factbase.add(Node(node_id, "level", level))
            items = [('column', node.column), ('filename', node.filename), ('line', node.line)]

        elif isinstance(node, Symbol):
            self.__factbase.add(Node(node_id, "type", "Symbol"))
            self.__factbase.add(Node(node_id, "level", level))
            self.__factbase.add(Node(node_id, "value", str(node)))

        elif isinstance(node, int):
            self.__factbase.add(Node(node_id, "type", "int"))
            self.__factbase.add(Node(node_id, "level", level))
            self.__factbase.add(Node(node_id, "value", node))

        elif isinstance(node, str):
            self.__factbase.add(Node(node_id, "type", "str"))
            self.__factbase.add(Node(node_id, "level", level))
            self.__factbase.add(Node(node_id, "value", node))

        else:
            raise Exception()

        # Recursively add descendants
        for key, val in items:
            self.add_node(val, parent_id=node_id, parent_key=key, level=level+1)


rast = ReifiedAST()
parse_files([sys.argv[1]], rast.add_node)

print(rast)
