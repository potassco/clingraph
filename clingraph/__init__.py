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
    attr = 'attr'

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

        def parse(value):
            self.type = value
            return True
        options.add(
            self.option_group,
            'type',
            'Rename the predicate that defines whether the graph is directed or undirected',
            parse,
            argument='<name>'
        )

        def parse(value):
            self.node = value
            return True
        options.add(
            self.option_group,
            'node',
            'Rename the predicate that defines nodes',
            parse,
            argument='<name>'
        )

        def parse(value):
            self.edge = value
            return True
        options.add(
            self.option_group,
            'edge',
            'Rename the predicate that defines edges',
            parse,
            argument='<name>'
        )

        def parse(value):
            self.attr = value
            return True
        options.add(
            self.option_group,
            'attr',
            'Rename the predicate that defines attributes',
            parse,
            argument='<name>'
        )

    def print_model(self, model, printer):
        types = []
        nodes = []
        edges = []
        attrs = {}

        for atom in model.symbols(shown=True):
            if atom.match(self.type, 1):
                types.append(str(atom.arguments[0]))

            elif any((atom.match(self.node, arity) for arity in [1, 2])):
                nodes.append(tuple(map(str, atom.arguments)))

            elif any((atom.match(self.edge, arity) for arity in [2, 3])):
                edges.append(tuple(map(str, atom.arguments)))

            elif atom.match(self.attr, 3):
                if atom.arguments[0].match('', 2):
                    key = tuple(map(str, atom.arguments[0].arguments))
                    attrs[key] = { str(atom.arguments[1]): str(atom.arguments[2]) }
                else:
                    key = str(atom.arguments[0])
                    attrs[key] = { str(atom.arguments[1]): str(atom.arguments[2]) }

        if types == ['digraph']:
            graph = Digraph()
        elif types == ['graph'] or types == []:
            graph = Graph()
        else:
            pass # TODO: Report an error.

        for node in nodes:
            graph.node(*node, _attributes=attrs.get(node[0]))

        for edge in edges:
            graph.edge(*edge, _attributes=attrs.get(edge[0:2]))

        print(graph.source)

        if self.view:
            graph.view(mktemp('.gv')) # TODO: Use a non-deprecated function.
