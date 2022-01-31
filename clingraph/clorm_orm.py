"""
    Defines an ORM for clingraphs using clorm
"""
import clorm
from clorm import Predicate, RawField, ComplexTerm, refine_field, ConstantField, SimpleField, Raw, FactBase
from clingo.symbol import Function
from clingraph.orm import ClingraphORM
from clingraph.exception import InvalidSyntax


class AttrID(ComplexTerm):
    # pylint: disable=missing-class-docstring
    attr_name = SimpleField
    attr_pos = SimpleField

    class Meta:
        is_tuple = True


ElementType = refine_field(ConstantField,
                           ["graph", "node", "edge", "graph_nodes", "graph_edges"])


class ClormORM(ClingraphORM):
    """
    Uses clorm as an ORM to query the facts defining the graph
    """
    # pylint: disable=too-many-instance-attributes

    def __init__(self, prefix: str = "", default_graph:str ="default"):
        """
        Defines the unifier classes based on the prefix

        Args:
            prefix (str): The prefix to all predicate names
        """
        # pylint: disable=missing-class-docstring
        class Graph(Predicate):
            id = RawField

            class Meta:
                name = prefix+"graph"

        class SubGraph(Predicate):
            id = RawField
            graph = RawField

            class Meta:
                name = prefix+"graph"

        class Node(Predicate):
            id = RawField
            graph = RawField

            class Meta:
                name = prefix+"node"

        class Edge(Predicate):
            id = RawField
            graph = RawField

            class Meta:
                name = prefix+"edge"

        class Attr(Predicate):
            element_type = ElementType
            element_id = RawField
            attr_id = AttrID.Field
            attr_value = RawField

            class Meta:
                name = prefix+"attr"

        class AttrSugar(Predicate):
            element_type = ElementType
            element_id = RawField
            attr_id = SimpleField
            attr_value = RawField

            class Meta:
                name = prefix+"attr"

        class NodeSugar(Predicate):
            id = RawField

            class Meta:
                name = prefix+"node"

        class EdgeSugar(Predicate):
            id = RawField

            class Meta:
                name = prefix+"edge"
        # pylint: disable=invalid-name

        self.Graph = Graph
        self.SubGraph = SubGraph
        self.Node = Node
        self.Edge = Edge
        self.Attr = Attr
        self.NodeSugar = NodeSugar
        self.EdgeSugar = EdgeSugar
        self.AttrSugar = AttrSugar

        self.default_graph = default_graph
        self.fb = FactBase()
        ClingraphORM.__init__(self,prefix)

    def __str__(self):
        """
        Returns the current set of facts as a string
        """
        return self.fb.asp_str()


    @property
    def unifiers(self):
        """
        The list of all unifiers
        """
        main_unifiers = [self.Graph, self.SubGraph,
                         self.Node, self.Edge, self.Attr]
        sugar_unifiers = [self.NodeSugar, self.EdgeSugar, self.AttrSugar]
        return main_unifiers+sugar_unifiers

    def get_element_class(self, element_type):
        """
        Obtains an element class for a type given as a string

        Args:
            element_type (str): graph, edge or node
        """
        if element_type == "edge":
            return self.Edge
        if element_type == "node":
            return self.Node
        if element_type == "graph":
            return self.Graph

        raise ValueError("Invalid element type")

    def add_fact_string(self, program):
        """
        Adds a string containing facts to the database

        Args:
            program (str): A string consisting of only facts, divided by a '.'
        """
        program = program.replace( '\\' ,'\\\\')

        try:
            fb = clorm.parse_fact_string(program, self.unifiers,raise_nonfact=True)
            self.add_to_fb(fb)
        except clorm.orm.symbols_facts.NonFactError as e:
            msg = "The input string contains a complex structure that is not a fact."
            raise InvalidSyntax(msg,str(e)) from None
        except RuntimeError as e:
            msg = "Syntactic error the input string can't be read as facts."
            raise InvalidSyntax(msg,str(e)) from None

    def add_fact_file(self, file):
        """
        Adds a file containing facts to the database

        Args:
            file (str): The path to the file
        """
        try:
            fb = clorm.parse_fact_files([file], self.unifiers,raise_nonfact=True)
            self.add_to_fb(fb)
        except clorm.orm.symbols_facts.NonFactError as e:
            msg = "The file contains a complex structure that is not a fact."
            raise InvalidSyntax(msg,str(e)) from None
        except RuntimeError as e:
            msg = "Syntactic error the file, can't be read as facts."
            raise InvalidSyntax(msg,str(e)) from None

    def add_clingo_model(self, model):
        """
        Adds a clingo model to the database

        Args:
            model (clingo.Model): A model returned by clingo
        """
        symbols = model.symbols(atoms=True, shown=True)
        fb = clorm.unify(self.unifiers, symbols)
        self.add_to_fb(fb)

    def add_to_fb(self, fb):
        """
        Adds a fact base to the current factbase
        """
        processed_fb = self.desugar(fb)
        self.fb = self.fb.union(processed_fb)

    def desugar(self, fb):
        """
        Desugar factbase
        - for each node(ID) add node(ID,default)  same for edge
        - replace attr(E,ID,Name,Val) with attr(E,ID,(Name,-1),Val)
        """
        q = fb.query(self.AttrSugar)
        for attr in set(q.all()):
            e = self.Attr(element_type=attr.element_type,
                          element_id=attr.element_id,
                          attr_value=attr.attr_value,
                          attr_id=AttrID(attr_name=attr.attr_id, attr_pos=-1))
            fb.remove(attr)
            fb.add(e)

        basic_element_classes = [
            (self.NodeSugar, self.Node), (self.EdgeSugar, self.Edge)]
        using_default = False
        for C_Sugar, C in basic_element_classes:
            q = fb.query(C_Sugar)
            for node in set(q.all()):
                using_default = True
                e = C(id=node.id,
                      graph=Raw(Function(self.default_graph)))
                fb.remove(node)
                fb.add(e)
        if using_default:
            fb.add(self.Graph(id=Raw(Function(self.default_graph))))

        return fb

    def get_all_graphs(self):
        """
        Gets a list if the identifiers for all the graphs
        """
        graph_ids = set([])
        q = self.fb.query(self.Graph).select(self.Graph.id)
        graph_ids = set(q.all())
        q = self.fb.query(self.SubGraph).select(self.SubGraph.id)
        graph_ids = graph_ids.union(set(q.all()))
        return graph_ids

    def parent_graph(self, graph_id):
        """
        Gets the parent graph for a given graph_id.
        Returns None if there is not such supertype

        Args:
            graph_id: Identifier of the subgraph
        """
        q = self.fb.query(self.SubGraph).where(self.SubGraph.id == graph_id)
        q = q.select(self.SubGraph.graph)
        if len(list(q.all())) == 0:
            return None
        return list(q.all())[0]

    def get_graph_global_element_attr(self, element_type, graph_id):
        """
        Gets the attributes for a global element: graph_nodes or graph_edges.
        Returns a dictionary where the keys are attribute name and values are
        attribute values.

        Args:
            element_type (str): The element type: 'edge' or 'node'
            graph_id: Identifier of the graph
        """
        full_element_type = f"graph_{element_type}s"
        return self.get_element_attr(full_element_type, graph_id)

    def get_graph_elements(self, element_type, graph_id):
        """
        Gets the list of elements for a graph

        Args:
            element_type (str): The element type: 'edge' or 'node'
            graph_id: Identifier of the graph
        """
        C = self.get_element_class(element_type)
        q = self.fb.query(C).where(C.graph == graph_id).select(C.id)
        return set(q.all())

    def get_element_attr(self, element_type, element_id):
        """
        Gets the attributes a specific element
        Returns a dictionary where the keys are attribute name and values are
        attribute values.

        Args:
            element_type (str): The element type: 'graph', 'edge' or 'node'
            element_id: Identifier of the element
        """
        q = self.fb.query(self.Attr)
        q = q.where(self.Attr.element_type == element_type,
                    self.Attr.element_id == element_id)
        # pylint: disable=no-member
        q = q.group_by(self.Attr.attr_id.attr_name)
        q = q.select(self.Attr.attr_id.attr_pos, self.Attr.attr_value)
        attrs = {}
        for name, list_opts in q.all():
            info = {"set": [], "idx": [], "sep": " "}
            for opt, val in list_opts:
                val_str = str(val).strip('"')
                if opt == "sep":
                    info["sep"] = val_str
                elif opt == -1:
                    info["set"].append(val_str)
                else:
                    i = int(opt)
                    if i >= len(info["idx"]):
                        info["idx"] = info["idx"] + \
                            [""]*(1+i-len(info["idx"]))
                    info["idx"][i] = val_str
            attrs[str(name)] = info["sep"].join(info["set"]+info["idx"]).replace('\\\\','\\')
        return attrs
