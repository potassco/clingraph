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
    """
    A clingo application to generate graphs from predicates
    """

    def __init__(self):
        self.program_name = 'clingraph'
        self.version = '0.1.0-dev'
        self.option_group = 'Clingraph Options'
        self.graphs = {}

        # Flags
        self.view = Flag(False)
        self.gif = Flag(False)
        self.model_as_postfix = Flag(False)

        # Arguments
        self.directory = 'out'
        self.format = 'gv'
        self.engine = 'dot'
        self.type = 'digraph'
        self.prefix = ''
        self.default_graph = 'default'

    def main(self, ctl, files):
        """
        Function to replace clingo's default main function.
        Arguments:
            ctl : Clingos control object
            files: The files passed to the application, that will generate the 
                    predicates representing the graph
        """
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
        return format in ['gv', 'pdf', 'svg', 'png']

    def _parse_engine(self, engine):
        self.engine = engine
        return engine in ["dot", "neato", "twopi", "circo", "fdp", "osage", "patchwork", "sfdp"]

    def _parse_prefix(self, prefix):
        self.prefix = prefix
        return not " " in prefix

    def _parse_default_graph(self, default_graph):
        self.default_graph = default_graph
        return not " " in default_graph

    def _parse_type(self, type):
        self.type = type
        return type in ['graph', 'digraph']

    def register_options(self, options):
        """
        Function to register custom options.
        Arguments:
            options: Object to register additional options
        """

        options.add(self.option_group, 'directory',
                    """Directory for saving and rendering 
         * Default: \out""",
                    self._parse_directory, argument='<str>')
        options.add(self.option_group, 'format',
                    """Rendering output format
        <arg>: {gv|pdf|png|svg} 
         * Default: gv (the graphsviz text format)""",
                    self._parse_format, argument='<arg>')
        options.add(self.option_group, 'type',
                    """Type of graph
        <arg> : {graph|digraph}
            graph: not-directed 
            digraph: directed 
         * Default: digraph""",
                    self._parse_type, argument='<arg>')
        options.add(self.option_group, 'engine',
                    """Layout command used 
        <arg>: {dot|neato|twopi|circo|fdp|osage|patchwork|sfdp}
         * Default: dot""",
                    self._parse_engine, argument='<arg>')
        options.add(self.option_group, 'prefix',
                    """Prefix used for the predicates to consider""",
                    self._parse_prefix, argument='<str>')
        options.add(self.option_group, 'default-graph',
                    """The name of the default graph 
        All nodes and edges with arity 1 will be assigned to this graph
         * Default: default""",
                    self._parse_default_graph, argument='<str>')
        options.add_flag(self.option_group, 'view',
                         """Render the answers and show them with the default
        viewer if they are images""",
                         self.view)
        options.add_flag(self.option_group, 'gif',
                         'Generate a gif from all graphs',
                         self.gif)
        options.add_flag(self.option_group, 'postfix',
                         """Saves output in the same directory using the model 
        number as postfix on the file name
         * Default: each stable model is saved in a different directory.""",
                         self.model_as_postfix)

    def model2structure(self, model):
        """
        Creates a dictionary with the graphs information from a model
        Arguments:
            model: The model obtained in the solving
        """
        elements = ['graph', 'node', 'edge']
        basic_info = {'graph': self.default_graph, 'attr': {}}
        graph_info = {'graph': None, 'node_attr': {},
                      'edge_attr': {}, 'attr': {}}
        structure = {
            'graph': defaultdict(lambda: copy.deepcopy(graph_info)),
            'node': defaultdict(lambda: copy.deepcopy(basic_info)),
            'edge': defaultdict(lambda: copy.deepcopy(basic_info))
        }
        structure['graph'][self.default_graph]

        def s2id(symbol, s_type=''):
            """
            Transforms a clingo symbol into a string
            """
            if s_type == 'edge':
                if len(symbol.arguments) != 2:
                    return ValueError("Edge should be a tuple of arity 2")
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
                if element_type in ['graph_nodes', 'graph_edges']:
                    subelement = element_type[-5:-1]
                    structure['graph'][element_id][subelement +
                                                   '_attr'][attr_name] = attr_value
                else:
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
        """
        Generates graphviz graphs from a dictionary structure
        Arguments:
            stucture: Dictionary with the structure of the graphs
        """
        # Create graphs
        graphs = {}
        dir_path = os.path.join(self.directory, f'model_{model_number}')
        if self.model_as_postfix:
            dir_path = self.directory
        for g_id, g in structure['graph'].items():
            if self.type == 'graph':
                _Graph = Graph
            elif self.type == 'digraph':
                _Graph = Digraph
            else:
                raise ValueError

            graph_name = g['attr']['name'] if 'name' in g['attr'] else g_id
            if self.model_as_postfix:
                graph_name += f'_{model_number}'

            graph = _Graph(
                name=f'{graph_name}',
                directory=dir_path,
                format=self.format,
                engine=self.engine,
                graph_attr=g['attr'],
                node_attr=g['node_attr'],
                edge_attr=g['edge_attr']
            )
            graphs[g_id] = graph

        # Add elements
        single_element = ['node', 'edge']
        default_used = False
        for e in single_element:
            for e_id, vals in structure[e].items():
                g = graphs[vals['graph']]
                default_used = default_used or vals['graph'] == self.default_graph
                if e == 'node':
                    g.node(e_id, **vals['attr'])
                else:
                    g.edge(e_id[0], e_id[1], **vals['attr'])

        if not default_used:
            del structure['graph'][self.default_graph]
            del graphs[self.default_graph]

        return graphs

    def model2graphs(self, model):
        """
        Construct the corresponing graphs from a model
        Arguments:
            model: Clingos stable model
        """
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
        """
        Saves the graphs
        """
        for _, graphs in self.graphs.items():
            for graph in graphs:
                render_format = self.format in ['pdf', 'svg', 'png']
                if render_format or self.view or self.gif:
                    graph.render(
                        view=self.view,
                        cleanup=True,
                        quiet_view=self.view,
                    )
                else:
                    if not os.path.exists(graph.directory):
                        os.makedirs(graph.directory)
                    with open(graph.filepath, "w+") as f:
                        f.write(graph.source)

            if self.gif:
                images = []
                for graph in graphs:
                    images.append(imageio.imread(
                        graph.filepath+"."+graph.format))
                imageio.mimsave(os.path.join(
                    graph.directory, 'movie.gif'), images, fps=1)

    def print_model(self, model, printer):
        """
        Function to print additional information when the text output is used.
        Arguments:
            model: Clingos stable model
        """
        print(model)
        print("\n" + "-"*20 + ' Clingraph ' + "-"*20 + "\n")
        graphs = self.model2graphs(model)
        self.graphs[model.number] = graphs
        self.save()
        for graph in self.graphs[model.number]:
            print(f"Output saved in {graph.filepath}")


def main():
    clingo_main(Clingraph())
