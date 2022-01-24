"""
    Definition of Clingraphs
"""
import clorm
import imageio
import logging
import os
import networkx as nx
from IPython import display
from fileinput import filename
from clorm import FactBase
from clingo import Model
from graphviz import Graph, Digraph
from clingraph.clorm_orm import ClormORM
LOG = logging.getLogger('custom')

class Clingraph:

    """
    A class to handndle graphs defined by facts
    """

    def __init__(self, type_: str = "graph", prefix: str = "", default_graph: str = "default"):
        """
        Creates a Clingraph object with the basic arguments
        Arguments:
            - type (str): Type of Graph, either "graph" or "digraph"
            - prefix (str): Prefix used in all the predicates cosidered in the module
            - default_graph (str): The name of the default graph all nodes and edges with arity 1 will be assigned to this graph
        """
        self.type_ = type_
        self.prefix = prefix
        self.default_graph = default_graph
        self.orm = ClormORM(self.prefix)
        self.graphs = {}  # All main graphs with corresponding nested subgraphs

    def __str__(self):
        """
        String representation of the clingraph
        """

        return self.source()

    def add_fact_string(self,  program: str):
        """
        Adds a program to the graph
        Arguments:
            - program (str): An string containing a list of facts separated with a `.`
        """
        LOG.debug(f"Adding string: {program}")
        self.orm.add_fact_string(program)

    def add_fact_file(self,  file: str):
        """
        Adds files to the graph
        Arguments:
            - file (str): The path to a file containing facts separated with a `.`
        """
        self.orm.add_fact_files(file)

    def add_model(self,  model: Model):
        """
        Adds a model to the graph. Can be use on the on_model function of clingo.
        Arguments:
            - model (clingo.Model): A clingo model
        """
        self.orm.add_clingo_model(model)

    def new_single_graph(self):
        """
        Creates a graphviz instance with the attribues
        """
        if self.type_ == 'graph':
            GraphClass = Graph
        else:
            GraphClass = Digraph

        return GraphClass()

    @property
    def facts(self):
        """
        Returns the facts as a string
        """
        return self.orm.get_fact_string()

    def source(self,selected_graphs=None):
        """
        Returns the source code of the select graphs
        """
        if len(self.graphs) == 0:
            return "// Graph hasn't been computed yet\n"
        if not selected_graphs:
            selected_graphs = list(self.graphs.keys())
        s = ""
        for g_name in selected_graphs:
            if g_name not in self.graphs:
                LOG.warn(f"Graph name: {g_name} not found, ignored")
                continue
            s += "//"+ "-"*10 + g_name + "-"*10 + "\n"
            s += self.graphs[g_name].source

        return s


    def compute_graphs(self):
        """
        Compute the graphs for the current factbase. Sets the value to graphs
        """
        graphs = self.orm.get_all_graphs()
        all_graphs = {}
        for g in graphs:
            graph = self.new_single_graph()
            graph.name = str(g).strip('"')

            graph.node_attr = self.orm.get_graph_global_element_attr("node", g)
            graph.edge_attr = self.orm.get_graph_global_element_attr("edge", g)
            graph.graph_attr = self.orm.get_element_attr("graph", g)

            elements = ["node", "edge"]
            for e_type in elements:
                element_ids = self.orm.get_graph_elements(e_type, g)
                for e in element_ids:
                    attr = self.orm.get_element_attr(e_type, e)
                    if e_type == 'node':
                        graph.node(str(e).strip('"'), **attr)
                    else:
                        graph.edge(str(e.symbol.arguments[0]).strip('"'),
                                   str(e.symbol.arguments[1]).strip('"'), **attr)

            all_graphs[graph.name] = graph

        self.graphs = self.nest_graphs(all_graphs)

    def nest_graphs(self, all_graphs):
        """
        Nests all_graphs by assigning subgraphs to graphs
        Arguments:
            all_graphs (dict): Dicionary of all the graphs to be nested
        """
        nested_graphs = {}
        graphs_ids = self.orm.get_all_graphs()
        parents_dic = {}
        for g_id in graphs_ids:
            g_name = str(g_id).strip('"')
            g = all_graphs[g_name]
            parent_id = self.orm.parent_graph(g_id)
            parent_name = str(parent_id).strip('"')
            parents_dic[g_name] = parent_name

        nx_g = nx.DiGraph(parents_dic.items())
        final_order = list(nx.topological_sort(nx_g))

        for g_name in final_order:
            if g_name == 'None':
                continue
            parent_name = parents_dic[g_name]
            g = all_graphs[g_name]
            if parent_name == 'None':
                nested_graphs[g_name] = g
                continue
            g_parent = all_graphs[parent_name]
            g.name = 'cluster_'+g.name
            g_parent.subgraph(g)

        return nested_graphs

    def save(self, directory, selected_graphs=None, format="pdf", name_prefix="", **kwargs):
        """
        Saves the graphs in the given directory.
        The files will be named using the graph identifier from the code.
        Arguments:
            directory: The path to save the files
            selected_graphs: The names of the graphs to be saved. By default all are saved
            format: Output format: 'pdf', 'svg', 'png'
            name_prefix: A prefix for the names of the file

            Any additional arguments are massed to the graphviz.render method
        """
        for graph_name, graph in self.graphs.items():
            if selected_graphs and graph_name not in selected_graphs:
                continue
            file_name = os.path.join(
                directory, f"{name_prefix}{graph_name}.{format}")
            graph.render(
                format=format,
                outfile=file_name,
                **kwargs,
                cleanup=True)
            LOG.info(f"Image saved in {file_name}")

    def save_gif(self, directory, name="clingraph", engine="dot",selected_graphs=None, **kwargs):
        """
        Creates a gif of all the graphs
        Arguments:
            directory: The path to save the files
            name: The name of the gif
            engine: A valid graphviz engine

            Any additional arguments are massed to the  imageio.mimsave method
        """
        images_dir = os.path.join(directory, 'images')
        self.save(images_dir,selected_graphs=selected_graphs, format="png", engine=engine)
        images = []
        file_name = os.path.join(directory, f'{name}.gif')
        for graph_name, _ in self.graphs.items():
            images.append(imageio.imread(
                os.path.join(images_dir, graph_name+".png")))
        imageio.mimsave(file_name,
                        images, **kwargs)

        LOG.info(f"Gif saved in {file_name}")

    def save_tex(self, directory, name_prefix=""):
        """
        Creates a tex file ussing dot2tex
        """
        return NotImplementedError

    def show(self, selected_graphs=None, **kwargs):
        """
        Shows the graphs in a frontend, such as jupyter
        Arguments:
            selected_graphs: The names of the graphs to be shown. By default all are shown

        """
        images_dir = 'out'
        self.save(images_dir, selected_graphs=selected_graphs, format="png", **kwargs)
        d = []
        for graph_name, graph in self.graphs.items():
            if selected_graphs and graph_name not in selected_graphs:
                continue
            d.append(graph_name)
            d.append(display.Image(os.path.join('out', graph_name+".png")))
        return display.display(*tuple(d))

    def show_gif(self, engine="dot", **kwargs):
        """
        Shows the a gif of the graphs
        Arguments:
            engine: A valid graphviz engine
            selected_graphs: The names of the graphs to be shown. By default all are shown

            Any additional arguments are massed to the  imageio.mimsave method
        """
        images_dir = 'out'
        self.save_gif(images_dir, engine=engine, **kwargs)
        return display.Image(os.path.join('out', "clingraph.gif"))
