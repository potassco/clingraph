"""
    Definition of Clingraphs
"""

import logging
import os
import networkx as nx
from clingo import Model
from graphviz import Graph, Digraph
from clingraph.clorm_orm import ClormORM
log = logging.getLogger('custom')

try:
    from IPython import display
    HAS_IPYTHON=True
except ImportError:
    HAS_IPYTHON=False

try:
    import dot2tex
    HAS_DOT2TEX=True
except ImportError:
    HAS_DOT2TEX=False

try:
    import imageio
    HAS_IMAGEIO=True
except ImportError:
    HAS_IMAGEIO=False

class Clingraph:

    """
    Clingraph contains the functionalities to transform sets of facts into graphviz objects that can be redered.
    """

    def __init__(self, type_: str = "graph", prefix: str = "", default_graph: str = "default", orm_class=ClormORM):
        """
        Creates a Clingraph object with the basic arguments

        Args:
            type (str): Type of Graph, either `graph` or `digraph`
            prefix (str): Prefix used in all the predicates \
                cosidered in the module
            default_graph (str): The name of the default graph \
                to which all nodes and edges with arity 1 will be assigned
            orm_class (ClingraphORM): A class that implements the :py:class:`ClingraphORM` class. \
                By default an implementation based on the tool ``clorm`` is used.
        """
        self.type_ = type_
        self.prefix = prefix
        self.default_graph = default_graph
        self._orm = orm_class(self.prefix, default_graph=default_graph)
        self._computed = False

        self._graphs = {}  # All main graphs with corresponding nested subgraphs

    def __str__(self):
        """
        String representation of the clingraph
        """

        return self.source()

    def add_fact_string(self,  program: str):
        """
        Adds a program to the graph

        Args:
            program (str): An string containing a list of facts separated with a dot(``.``)

        Raises:
            InvalidSyntax: If the string can't be read as facts
        """
        log.debug("Adding string: %s", program)
        self._orm.add_fact_string(program)

    def add_fact_file(self,  file: str):
        """
        Adds files to the graph

        Args:
            file (str): The path to a file containing facts separated with a a dot(``.``)

        Raises:
            InvalidSyntax: If the file contains something other than facts
        """
        self._orm.add_fact_file(file)

    def add_model(self,  model: Model):
        """
        Adds a model to the graph. Can be use on the `on_model` function of clingo.
        To handle multiple models see :py:class`MultiModelClingraph`.

        Args:
            model (clingo.Model): A clingo model
        """
        self._orm.add_clingo_model(model)

    def _new_single_graph(self):
        """
        Creates a graphviz instance with the attributes
        """
        if self.type_ == 'graph':
            GraphClass = Graph
        else:
            GraphClass = Digraph

        return GraphClass()

    def _check_computed(self):
        """
        Raises an error if the graphs haven't been computed yet
        """

        if not self._computed:
            raise RuntimeError("Can't obtain the graphviz object before computing the graphs")

    def get_graphviz(self, graph_name=None):
        """
        Obtains a graphviz object for the given graph name.
        If no graph_name is passed then the default graph will be returned

        Args:
            graph_name (str): The graph name defined in predicate ``graph(NAME).``

        Returns:
            A graphviz object

        Raises:
            RuntimeError: When the graph hasn't been computed yet
            ValueError: If the graph name is not valid
        """
        self._check_computed()
        if graph_name is None:
            graph_name = self.default_graph
        if not graph_name in self._graphs:
            raise ValueError(f"No graph with name '{graph_name}' found.")
        return self._graphs[graph_name]

    def _get_graphvizs(self, graph_names=None):
        """
        Obtains a list of graphvizs by name

        Args:
            graph_names (list): A list with the graph names defined in predicate ``graph(NAME).``

        Returns:
            A dictionary of graphviz object. A subset of the graphs attribute.

        Raises:
            RuntimeError: When the graph hasn't been computed yet
            ValueError: If the graph name is not valid
        """
        self._check_computed()
        if graph_names is None:
            return self._graphs
        return {str(g_name):self.get_graphviz(g_name) for g_name in graph_names}

    def get_facts(self):
        """
        Returns the current set of facts as a string

        Returns:
            A string containing all the facts after preprocessing
        """
        return str(self._orm)

    def source(self,selected_graphs=None):
        """
        Returns the source code of the select graphs.

        Args:
            selected_graphs (list): The names of the graphs to be shown. By default all are selected.

        Returns:
            A string containing the graphviz source code for the selected graphs.
            If no graphs are selected will return the source of all graphs.
        """
        if not self._computed:
            return "// Graph hasn't been computed yet\n"
        if len(self._graphs) == 0:
            return "// Empty clingraph\n"
        graphs = self._get_graphvizs(selected_graphs)
        s = ""
        for g_name in graphs:
            s += "//"+ "-"*10 + g_name + "-"*10 + "\n"
            s += self._graphs[g_name].source

        return s


    def compute_graphs(self):
        """
        Compute the graphs for the current list of facts.
        It creates a Graphviz instance for each graph defined by the facts.
        Graphs can then be obtained by name using the method :py:meth:`get_graphviz`.
        """
        if self._computed:
            log.warning("Graph already computed, but will be computed again")

        graphs = self._orm.get_all_graphs()
        all_graphs = {}
        for g in graphs:
            graph = self._new_single_graph()
            graph.name = str(g).strip('"')

            graph.node_attr = self._orm.get_graph_global_element_attr("node", g)
            graph.edge_attr = self._orm.get_graph_global_element_attr("edge", g)
            graph.graph_attr = self._orm.get_element_attr("graph", g)

            elements = ["node", "edge"]
            for e_type in elements:
                element_ids = self._orm.get_graph_elements(e_type, g)
                for e in element_ids:
                    attr = self._orm.get_element_attr(e_type, e)
                    if e_type == 'node':
                        graph.node(str(e).strip('"'), **attr)
                    else:
                        graph.edge(str(e.symbol.arguments[0]).strip('"'),
                                   str(e.symbol.arguments[1]).strip('"'), **attr)

            all_graphs[graph.name] = graph

        self._graphs = self._nest_graphs(all_graphs)
        self._computed = True

    def _nest_graphs(self, all_graphs):
        """
        Nests all_graphs by assigning subgraphs to graphs

        Args:
            all_graphs (dict): Dictionary of all the graphs to be nested
        """
        nested_graphs = {}
        graphs_ids = self._orm.get_all_graphs()
        parents_dic = {}
        for g_id in graphs_ids:
            g_name = str(g_id).strip('"')
            g = all_graphs[g_name]
            parent_id = self._orm.parent_graph(g_id)
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

    def save(self, directory='out', selected_graphs=None, format="pdf", name_prefix="", **kwargs):
        # pylint: disable=redefined-builtin

        """
        Saves the graphs in the given directory.
        The files will be named using the graph identifier in the predicate.

        Args:
            directory (str): The path to save the files
            selected_graphs (list): The names of the graphs to be saved. By default all are saved
            format (str): Output format: `pdf`, `svg` or `png`
            name_prefix (str): A prefix for the names of the file

        Any additional arguments are passed to the `graphviz.render` method

        Raises:
            RuntimeError: When the graph hasn't been computed yet

        """
        graphs = self._get_graphvizs(selected_graphs)

        for graph_name, graph in graphs.items():
            file_name = os.path.join(
                directory, f"{name_prefix}{graph_name}.{format}")
            graph.render(
                format=format,
                directory=directory,
                filename=f"{name_prefix}{graph_name}",
                **kwargs,
                cleanup=True)
            log.info("Image saved in %s",file_name)

    def save_gif(self, directory='out', name="clingraph", engine="dot",selected_graphs=None, **kwargs):
        """
        Creates a gif of all the graphs

        Args:
            directory: The path to save the files
            name: The name of the gif
            engine: A valid graphviz engine

            Any additional arguments are passed to the  imageio.mimsave method
        """
        if not HAS_IMAGEIO:
            raise RuntimeError("imageio module has to be installed to save gifs")

        graphs = self._get_graphvizs(selected_graphs)

        images_dir = os.path.join(directory, 'images')
        self.save(images_dir,selected_graphs=selected_graphs, format="png", engine=engine)
        images = []
        file_name = os.path.join(directory, f'{name}.gif')
        for graph_name in graphs:
            images.append(imageio.imread(
                os.path.join(images_dir, graph_name+".png")))
        imageio.mimsave(file_name,
                        images, **kwargs)

        log.info("Gif saved in %s", file_name)

    def save_tex(self, directory="out", name_prefix="", selected_graphs=None, **kwargs):
        """
        Creates a tex file ussing dot2tex
        """
        if not HAS_DOT2TEX:
            raise RuntimeError("dot2tex module has to be installed to export to tex")
        graphs = self._get_graphvizs(selected_graphs)
        for graph_name, g in graphs.items():
            source = g.source

            texcode = dot2tex.dot2tex(source, **kwargs)

            file_name = os.path.join(directory, f'{name_prefix}{graph_name}.tex')

            with open(file_name,'w',encoding='utf-8') as f:
                f.write(texcode)

            log.info("Latex file saved in %s",file_name)

    def _show(self, selected_graphs=None, **kwargs):
        """
        Shows the graphs in a frontend, such as jupyter

        Args:
            selected_graphs: The names of the graphs to be shown. By default all are shown

        """
        if not HAS_IPYTHON:
            raise RuntimeError("ipython module has to be installed to display images")
        graphs = self._get_graphvizs(selected_graphs)
        images_dir = 'out'
        self.save(images_dir, selected_graphs=selected_graphs, format="png", **kwargs)
        d = []
        for graph_name in graphs:
            d.append(graph_name)
            d.append(display.Image(os.path.join('out', graph_name+".png")))
        return display.display(*tuple(d))

    def _repr_html_(self):
        """
        Shows the graphs in a frontend, such as jupyter
        """
        return self._show()

    def show_gif(self, selected_graphs=None, engine="dot", **kwargs):
        """
        Shows the a gif of the graphs

        Args:
            engine (str): A valid graphviz engine
            selected_graphs (list): The names of the graphs to be shown. By default all are shown

        Any additional arguments are passed to the ``imageio.mimsave`` method
        """
        images_dir = 'out'
        self.save_gif(images_dir, engine=engine,selected_graphs=selected_graphs, **kwargs)
        return display.Image(os.path.join('out', "clingraph.gif"))
