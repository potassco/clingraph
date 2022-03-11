
"""
Graphviz integration to generate latex
"""

from .utils import apply
try:
    import dot2tex
except ImportError:
    raise RuntimeError("dot2tex module has to be installed to export to tex") from None


def _to_tex(g, **kwargs):
    """
    Gets the source of a graphviz object
    """
    return dot2tex.dot2tex(g.source, **kwargs)

def tex(graphs, **kwargs):
    """
    Generates the latex code for the graphs

    Args:
        graphs (dic|list[dic]): A dictionary of graphviz objects where the keys are the graph names.
                Or a list of such dictionaries, each element corresponding to a model.
        **kwargs: Any additional arguments passed to dot2tex ``dot2tex()`` function

    Returns: (dic|list[dic]) The dictionary or list with a string containing the latex code instead of the graphviz objects.
    """
    return apply(graphs, _to_tex, **kwargs)
