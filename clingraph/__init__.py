from clingo.application import Application, clingo_main, Flag
from clingo.symbol import Function
from graphviz import Graph, Digraph
from collections import defaultdict

class Clingraph(Application):
    program_name = 'clingraph'
    version = '0.1.0-dev'

    option_group = 'Clingraph Options'

    render = Flag(False)
    view = Flag(False)

    directory = 'out'
    format = None
    engine = None

    prefix = ''

    def main(self, ctl, files):
        for path in files:
            ctl.load(path)
        if not files:
            ctl.load('-')
        ctl.ground([('base', [])], context=self)
        ctl.solve()

    def parse_directory(self, dir):
        self.directory = dir
        #TODO check that it is actually a directory
        return True
    
    def parse_format(self, format):
        self.format = format
        return format in ['pdf','svg','png']

    def parse_engine(self, engine):
        self.engine = engine
        return engine in ["dot", "neato", "twopi", "circo", "fdp", "osage", "patchwork", "sfdp"]

    def parse_prefix(self, prefix):
        self.prefix = prefix
        return not " " in prefix

    def register_options(self, options):
        # TODO add default
        options.add_flag(self.option_group, 'render', 
            'Render the answers', self.render)
        options.add_flag(self.option_group, 'view', 
            'Render the answers and show them with the default viewer', self.view)
        options.add(self.option_group, 'directory', 
            'Directory for source saving and rendering', self._parse_directory, argument='<path>' )
        options.add(self.option_group, 'format', 
            'Rendering output format', self._parse_format, argument='<format>' )
        options.add(self.option_group, 'engine', 
            'Layout command used', self._parse_engine, argument='<engine>' )
        options.add(self.option_group, 'prefix', 
            'Prefix used for the predicates that the package will consider', self._parse_prefix, argument='<engine>' )

    def model2graphs(self, model):
        elements = ['graph','cluster','class','node','edge']
        basic_info = {'graph': 'default','cluster': None, 'attr': {}}
        structure = {
            'graph': defaultdict(lambda: {'attr': [('type','graph')]}.copy()),
            'cluster': defaultdict(lambda: basic_info.copy()),
            'class': defaultdict(lambda: basic_info.copy()),
            'node': defaultdict(lambda: basic_info.copy()),
            'edge': defaultdict(lambda: basic_info.copy())
        }
        structure['graph']['default']
        structure['class']['node']
        structure['class']['edge']

        for atom in model.symbols(atoms=True):
            if not atom.startswith(self.prefix):
                continue
            name = atom.name
            if atom.match(self.prefix+"attr", 4):
                #TODO maybe nicer way to treat integers
                element_type = str(atom[0]).strip('"')
                element_id = str(atom[1]).strip('"')
                attr_name = str(atom[2]).strip('"')
                attr_value = str(atom[3]).strip('"')
                if attr_name in ['graph','cluster']:
                    structure[attr_name][attr_value]
                    structure[element_type][element_id][attr_name]=attr_value
                else:
                    structure[element_type][element_id]['attr'][attr_name]=attr_value
                continue
            for e in elements:
                if atom.match(self.prefix+e,1):
                    structure[e]
                    continue

        for g_id, g in structure['graph'].items():
            if g['attr']['type'] == 'graph':
                _Graph = Graph
            elif g['attr']['type'] == 'digraph':
                _Graph = Digraph
            else: raise ValueError

            graph_name = g['attr']['name'] if 'name' in  g['attr'] else g_id
            graph = _Graph(
                name = f'{graph_name}_{model.number:04d}',
                directory = self.directory,
                format = self.format,
                engine = self.engine,
                graph_attr = g['attr'],
                node_attr = structure['class']['node'],
                edge_attr = structure['class']['edge']
            )
        

    def print_model(self, model, printer):
        types = []
        nodes = []
        edges = []
        attrs = { 'graph': {}, 'node': {}, 'edge': {} }

        for atom in model.symbols(shown=True):
            if atom.match(self.type, 1):
                types.append(str(atom.arguments[0]))

            elif atom.name == self.node and len(atom.arguments) in [1, 2]:
                nodes.append(tuple(map(str, atom.arguments)))

            elif atom.name == self.edge and len(atom.arguments) in [2, 3]:
                edges.append(tuple(map(str, atom.arguments)))

            elif atom.match(self.attr, 3):
                entity = atom.arguments[0]
                if entity.name in ['graph', 'node', 'edge'] and len(entity.arguments) == 0:
                    entity = entity.name
                elif entity.match('node', 1) or entity.match('edge', 2):
                    entity = tuple(map(str, entity.arguments))
                else: raise ValueError

                key = str(atom.arguments[1])
                val = str(atom.arguments[2])

                if entity not in attrs:
                    attrs[entity] = {}

                attrs[entity][key] = val

        if types in [[], ['graph']]:
            _Graph = Graph
        elif types in [['digraph']]:
            _Graph = Digraph
        else: raise ValueError

        graph = _Graph(
            name = f'{model.number:04d}',
            directory = self.directory,
            format = self.format,
            engine = self.engine,
            graph_attr = attrs['graph'],
            node_attr = attrs['node'],
            edge_attr = attrs['edge'],
        )

        for node in nodes:
            graph.node(*node, _attributes=attrs.get(node[0:1]))

        for edge in edges:
            graph.edge(*edge, _attributes=attrs.get(edge[0:2]))

        if self.render or self.view:
            path = graph.render(
                view=self.view,
                cleanup=True,
                quiet_view=self.view,
            )
            print(f'Saved to {path}')
        else:
            print(graph.source)

def main():
    clingo_main(Clingraph())
