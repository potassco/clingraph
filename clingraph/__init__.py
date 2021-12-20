import imageio
import os
import copy
import networkx as nx
from collections import defaultdict
from graphviz import Graph, Digraph
from clingo.application import Application, clingo_main, Flag
from clingo.symbol import Function, String
from clingo.script import enable_python
enable_python()


class Clingraph(Application):

    def __init__(self):
        self.program_name = 'clingraph'
        self.version = '0.1.0-dev'
        self.option_group = 'Clingraph Options'
        self.graphs = {}

        # Flags
        self.render = Flag(False)
        self.view = Flag(False)
        self.gif = Flag(False)
        self.model_as_postfix = Flag(False)

        # Arguments
        self.directory = 'out'
        self.format = 'pdf'
        self.engine = 'dot'
        self.prefix = ''


    def main(self, ctl, files):
        for path in files:
            ctl.load(path)
        if not files:
            ctl.load('-')
        ctl.ground([('base', [])])
        ctl.solve()       

    def _parse_directory(self, dir):
        self.directory = dir
        return True

    def _parse_format(self, format):
        self.format = format
        return format in ['pdf', 'svg', 'png']

    def _parse_engine(self, engine):
        self.engine = engine
        return engine in ["dot", "neato", "twopi", "circo", "fdp", "osage", "patchwork", "sfdp"]

    def _parse_prefix(self, prefix):
        self.prefix = prefix
        return not " " in prefix


    def register_options(self, options):
        options.add_flag(self.option_group, 'render',
                         'Render the answers', self.render)
        options.add_flag(self.option_group, 'view',
                         'Render the answers and show them with the default viewer', self.view)
        options.add_flag(self.option_group, 'gif',
                         'Generate a gif from all graphs', self.gif)
        options.add_flag(self.option_group, 'postfix',
                         'Saves output in the same directory using the model number as postfix on the file name', self.model_as_postfix)
        options.add(self.option_group, 'directory',
                    'Directory for source saving and rendering', self._parse_directory, argument='<path>')
        options.add(self.option_group, 'format',
                    'Rendering output format', self._parse_format, argument='<format>')
        options.add(self.option_group, 'engine',
                    'Layout command used', self._parse_engine, argument='<engine>')
        options.add(self.option_group, 'prefix',
                    'Prefix used for the predicates that the package will consider', self._parse_prefix, argument='<engine>')

    def model2structure(self, model):
        elements = ['graph', 'class', 'node', 'edge']
        basic_info = {'graph': 'default', 'attr': {}}
        graph_info = {'graph': None, 'attr': {'type': 'graph'}}
        structure = {
            'graph': defaultdict(lambda: copy.deepcopy(graph_info)),
            'class': defaultdict(lambda: copy.deepcopy(basic_info)),
            'node': defaultdict(lambda: copy.deepcopy(basic_info)),
            'edge': defaultdict(lambda: copy.deepcopy(basic_info))
        }
        structure['graph']['default']
        structure['class']['node']
        structure['class']['edge']

        # TODO maybe nicer way to treat integers than s2id function
        def s2id(symbol, type=''):
            if type == 'edge':
                if len(symbol.arguments) != 2:
                    # TODO handle errors better
                    return ValueError
                return tuple([str(a).strip('"') for a in symbol.arguments])
            return str(symbol).strip('"')

        for atom in model.symbols(atoms=True, shown=True):
            name = atom.name
            if not name.startswith(self.prefix):
                continue
            if atom.match(self.prefix+"attr", 4):
                args = atom.arguments
                element_type = s2id(args[0])
                element_id = s2id(args[1], element_type)
                attr_name = s2id(args[2])
                attr_value = s2id(args[3])
                structure[element_type][element_id]['attr'][attr_name] = attr_value
            for e in elements:
                if atom.match(self.prefix+e, 1):
                    structure[e][s2id(atom.arguments[0], e)]
                    continue
                if atom.match(self.prefix+e, 2):
                    structure[e][s2id(atom.arguments[0], e)
                                ]['graph'] = s2id(atom.arguments[1])
                    continue

        return structure

    def structure2graphs(self, structure, model_number):
        # Create graphs
        graphs = {}
        dir_path = os.path.join(self.directory, f'model_{model_number}')
        if self.model_as_postfix:
            dir_path=self.directory
        for g_id, g in structure['graph'].items():
            if g['attr']['type'] == 'graph':
                _Graph = Graph
            elif g['attr']['type'] == 'digraph':
                _Graph = Digraph
            else:
                raise ValueError

            graph_name = g['attr']['name'] if 'name' in g['attr'] else g_id
            if self.model_as_postfix:
                graph_name += f'_{model_number}'
            
            node_attr = {}
            edge_attr = {}
            
            if g['graph'] is None: #is not a subgraph
                node_attr = structure['class']['node']['attr']
                edge_attr = structure['class']['edge']['attr']

            graph = _Graph(
                name=f'{graph_name}',
                directory=dir_path,
                format=self.format,
                engine=self.engine,
                graph_attr=g['attr'],
                node_attr=node_attr,
                edge_attr=edge_attr
            )
            graphs[g_id] = graph

        # Add elements
        single_element = ['node', 'edge']
        default_used = False
        for e in single_element:
            for e_id, vals in structure[e].items():
                g = graphs[vals['graph']]
                default_used = default_used or vals['graph'] == 'default'
                if 'class' in vals['attr']:
                    class_attr = structure['class'][vals['attr']
                                                    ['class']]['attr'].copy()
                else:
                    class_attr = {}
                if e == 'node':
                    g.node(e_id, **({**class_attr, **vals['attr']}))
                else:
                    g.edge(e_id[0], e_id[1], **({**class_attr, **vals['attr']}))

        if not default_used:
            del structure['graph']['default']
            del graphs['default']

        return graphs

    def model2graphs(self, model):
        
        structure = self.model2structure(model)
        
        graphs = self.structure2graphs(structure, f'{model.number:04d}')

        # Attach subgraphs
        final_graphs = []
        graph_order = [(g_id, g['graph'] or 'top')
                       for g_id, g in structure['graph'].items()]
        nx_g = nx.DiGraph(graph_order)
        final_order = list(nx.topological_sort(nx_g))

        for g_id in final_order:
            if g_id == 'top':
                continue

            g_parent = structure['graph'][g_id]['graph']
            g = graphs[g_id]
            if g_parent is None:
                final_graphs.append(g)
                continue
            g.name = 'cluster_'+g.name
            graphs[g_parent].subgraph(g)

        return final_graphs

    def save(self):
        for _, graphs in self.graphs.items():
            for graph in graphs:
                if self.render or self.view or self.gif:
                    graph.render(
                        view=self.view,
                        cleanup=True,
                        quiet_view=self.view,
                    )
                else:
                    with open(graph.filepath, "w") as f:
                        f.write(graph.source)
            
            if self.gif:
                images = []
                for graph in graphs:
                    images.append(imageio.imread(
                        graph.filepath+"."+graph.format))
                imageio.mimsave(os.path.join(
                    graph.directory, 'movie.gif'), images, fps=1)

                    
    def print_model(self, model, printer):
        print(model)
        print("\n" + "-"*20 + ' Clingraph ' + "-"*20 + "\n")
        graphs = self.model2graphs(model)
        self.graphs[model.number] = graphs
        self.save()
        for graph in self.graphs[model.number]:
            print(f"Output saved in {graph.filepath}")


def main():
    clingo_main(Clingraph())
