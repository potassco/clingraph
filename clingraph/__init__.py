from clingo.application import Application, Flag
from clingo.symbol import Function
from graphviz import Graph, Digraph
from tempfile import mktemp

class Clingraph(Application):
    program_name = 'clingraph'
    version = '0.1.0-dev'

    option_group = 'Clingraph Options'

    view = Flag(False)

    type = 'type'
    node = 'node'
    edge = 'edge'

    def main(self, ctl, files):
        for path in files:
            ctl.load(path)
        if not files:
            ctl.load('-')
        ctl.ground([('base', [])], context=self)
        ctl.solve()

    def register_options(self, options):
        options.add_flag(
            self.option_group,
            'show',
            'Render models and show them with the default viewer',
            self.view
        )

        def parse(str):
            self.type = str
            return True
        options.add(
            self.option_group,
            'type',
            'Rename the predicate that defines whether the graph is directed or undirected',
            parse,
            argument='<name>'
        )

        def parse(str):
            self.node = str
            return True
        options.add(
            self.option_group,
            'node',
            'Rename the predicate that defines nodes',
            parse,
            argument='<name>'
        )

        def parse(str):
            self.edge = str
            return True
        options.add(
            self.option_group,
            'edge',
            'Rename the predicate that defines edges',
            parse,
            argument='<name>'
        )

    def print_model(self, model, printer):
        if model.contains(Function(self.type, [Function('digraph')])):
            graph = Digraph()
        else:
            graph = Graph()

        for atom in model.symbols(shown=True):
            if atom.name == self.node and len(atom.arguments) in [1, 2]:
                graph.node(*map(str, atom.arguments))
            if atom.name == self.edge and len(atom.arguments) in [2, 3]:
                graph.edge(*map(str, atom.arguments))

        print(graph.source)

        if self.view:
            graph.view(mktemp('.gv')) # TODO: Use a non-deprecated function.
