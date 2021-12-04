from clingo.application import Application
from clingo.symbol import Function
from graphviz import Graph

TYPE = 'clingraph_type'
TYPE_GRAPH = 'graph'
TYPE_DIGRAPH = 'digraph'

NODE = 'clingraph_node'
EDGE = 'clingraph_edge'

class Clingraph(Application):
    program_name = 'clingraph'
    version = '0.1.0-dev'

    def main(self, ctl, files):
        for path in files:
            ctl.load(path)
        if not files:
            ctl.load('-')
        ctl.ground([('base', [])], context=self)
        ctl.solve()

    def print_model(self, model, printer):
        if model.contains(Function(TYPE, [Function(TYPE_DIGRAPH)])):
            graph = Digraph()
        else:
            graph = Graph()

        for atom in model.symbols(shown=True):
            if atom.name == NODE and len(atom.arguments) == 1:
                graph.node(str(atom.arguments[0]))
            if atom.name == EDGE and len(atom.arguments) == 2:
                graph.edge(
                    str(atom.arguments[0]),
                    str(atom.arguments[1])
                )

        print(graph.source)
