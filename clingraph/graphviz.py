"""
Graphviz functionality
"""
import os
import logging
import networkx as nx
from graphviz import Graph, Digraph
from .utils import apply
log = logging.getLogger('custom')


def _nest_graphs(fb, all_graphs):
    """
    Nests all_graphs by assigning subgraphs to graphs

    Args:
        fb (Factbase): The Factbase
        all_graphs (dict): Dictionary of all the graphs to be nested
    """
    nested_graphs = {}
    graphs_ids = fb.get_all_graphs()
    parents_dic = {}
    for g_id in graphs_ids:
        g_name = str(g_id).strip('"')
        g = all_graphs[g_name]
        parent_id = fb.get_parent_graph(g_id)
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

def _compute_graphs_single_fb(fb, graphviz_type = 'graph',seed=None):
    """
    Compute the graphs for the factbase.
    It creates a Graphviz instance for each graph defined by the facts.
    Graphs can then be obtained by name using the method :py:meth:`get_graphviz`.
     Args:
        fb (:class:`Factbase`): A :class:`Factbase` to generate the graphviz objects.
        graphviz_type (str): The type of graph ``graph`` for ``graphviz.Graph`` and ``digraph`` for ``graphviz.Digraph``
        seed (int): A number used as seed
    """
    graphs = fb.get_all_graphs()
    all_graphs = {}
    for g in graphs:
        if graphviz_type == 'graph':
            GraphClass = Graph
        else:
            GraphClass = Digraph
        graph = GraphClass()
        graph.name = str(g).strip('"')

        graph.node_attr = fb.get_graph_global_element_attr("node", g)
        graph.edge_attr = fb.get_graph_global_element_attr("edge", g)
        graph_attr = {"start":seed} if seed is not None else {}
        graph_attr.update(fb.get_element_attr("graph", g))
        graph.graph_attr = graph_attr

        elements = ["node", "edge"]
        for e_type in elements:
            element_ids = fb.get_graph_elements(e_type, g)
            for e in element_ids:
                attr = fb.get_element_attr(e_type, e)
                if e_type == 'node':
                    graph.node(str(e).strip('"'), **attr)
                else:
                    graph.edge(str(e.symbol.arguments[0]).strip('"'),
                                str(e.symbol.arguments[1]).strip('"'), **attr)

        all_graphs[graph.name] = graph

    graphs = _nest_graphs(fb, all_graphs)
    return graphs

def compute_graphs(fb, graphviz_type = 'graph', seed=None):
    """
    Computes graphs using Graphviz for the given factbase

    Args:
        fb (list[:class:`Factbase`] | :class:`Factbase`): A :class:`Factbase` to generate the graphviz objects.
            If a list is passed, each element is cosidered as the Factbase for a stable model.
        graphviz_type (str): The type of graph ``graph`` for ``graphviz.Graph`` and ``digraph`` for ``graphviz.Digraph``
        seed (int): A number used as seed
    """
    is_multi_model = isinstance(fb,list)
    if not is_multi_model:
        fb = [fb]
    result = []
    for f in fb:
        if f is None:
            result.append(None)
        else:
            result.append(_compute_graphs_single_fb(f,graphviz_type=graphviz_type,seed=seed))
    if not is_multi_model:
        return result[0]
    return result

def _render_single_graph(graph, directory, format,engine,view, name_format=None):
    """
    Render a graphviz object

    Args:
        graph (str): A graphviz object
        directory (str): Where to save the object
        format (str): The format for the output ``pdf``, ``png`` or ``svg``
        name_format (str): The format for the name
        **kwargs: Any additional arguments passed to graphviz ``render()`` function

    Returns:
        str: The path where the image was saved
    """
    #pylint: disable=redefined-builtin
    assert isinstance(graph,(Graph,Digraph))
    file_name = name_format
    file_path = os.path.join(
        directory, f"{file_name}.{format}")
    graph.engine = engine
    graph.render(
        format=format,
        directory=directory,
        filename=file_name,
        # engine=engine,
        view=view,
        cleanup=True)
    return file_path

def render(graphs, directory="out", format="pdf", name_format=None,engine='dot',view=False):
    """
    Render the given graphviz graphs that where computed using :func:`compute_graphs`.

    Args:
        graphs (dic|list[dic]): A dictionary of graphviz objects where the keys are the graph names.
                Or a list of such dictionaries, each element corresponding to a model.
        directory (str): Where to save the object
        format (str): The format for the output ``pdf``, ``png`` or ``svg``
        name_format (str): The format for the name.
        engine (str): Engine used for the layout
        view (bool): If the rendered files will be oppend

    Returns:
        [dic | list[dic]]: A dictionary with the paths where the images where saved as values for each graph.
                Or a list of such dictionaries, each element corresponding to a model.
    """
    #pylint: disable=redefined-builtin
    return apply(graphs, _render_single_graph,
            directory=directory,
            format=format,
            name_format=name_format,
            engine=engine,
            view=view)


def dot(graphs):
    """
    Gets the source string in dot language for the graphs

    Args:
        graphs (dic|list[dic]): A dictionary of graphviz objects where the keys are the graph names.
                Or a list of such dictionaries, each element corresponding to a model.
    """
    return apply(graphs, lambda g: g.source)
