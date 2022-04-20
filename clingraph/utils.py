"""
Utils functions used across the project
"""
import os
import logging
log = logging.getLogger('custom')

def apply(elements, function,**kwargs):
    """
    Applies a given function to the elements.

    Args:
        elements (list[dic]|dic): A dictionary where the keys are considered the graph names
                and  the function is applied to the values.
                Can also be a list of such dictionaries, where each element is considered a model.
                Any ``None`` values in the list will be skiped.
        function (callable): The function to be applied
        **kwargs: Any arguments passed to the function. If an argument ``name_format`` is passed,
                ``{graph_name}`` and ``{model_number}`` will be substituted in this string by the
                corresponding values during the iteration.

    Returns: (list[dic]|[dic]) The elements after appling the function to the values
    """
    is_multi_model = isinstance(elements,list)
    if not is_multi_model:
        elements = [elements]
    name_format = None
    if 'name_format' in kwargs:
        if kwargs['name_format'] is None:
            name_format = "{graph_name}"
        else:
            name_format=kwargs['name_format']
        if len(elements)>1 and '{model_number}' not in name_format:
            log.warning("Output files will be overwritten since no `{model_number}` is used in the name format argument.")
    result = []
    for i,d in enumerate(elements):
        if d is None:
            result.append(None)
            continue
        element_result = {}
        for graph_name, e in d.items():
            if name_format:
                kwargs["name_format"]=name_format.replace('{graph_name}', graph_name).replace('{model_number}',str(i))
            element_result[graph_name]= function(e, **kwargs)
        result.append(element_result)

    if not is_multi_model:
        return result[0]
    return result

def _write(info, directory, format, name_format):
    """
    Writes the string info

    Args:
        directory (str): Path to the directory where to write
        format (str): Output format
        name_format (str): The file name
    """
    #pylint: disable=redefined-builtin
    file_name = name_format
    file_path = os.path.join(
        directory, f"{file_name}.{format}")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path,'w',encoding='utf-8') as f:
        f.write(info)
    return file_path

def write(elements, directory, format, name_format=None):
    """
    Writes all the elements info using :py:func:`apply`

    Args:
        elements (list|dic): A dictionary where the keys are considered the graph names
                and  the write is applied to the values.
                Can also be a list of such dictionaries, where each element is considered a model.
        directory (str): Path to the directory where to write
        format (str): Output format
        name_format (str): The file name

    Returns:
        [dic | list[dic]]: A dictionary with the paths where the files where saved as values for each graph.
                Or a list of such dictionaries, each element corresponding to a model.
    """
    #pylint: disable=redefined-builtin
    return apply(elements, _write,
            directory = directory,
            format = format,
            name_format=name_format)
