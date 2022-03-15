"""
Utils functions used across the project
"""
import json
import os
import logging
import jsonschema
from jsonschema import validate
from .exceptions import InvalidSyntax, InvalidSyntaxJSON
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
    print(f"File saved in {file_path}")

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
    """
    #pylint: disable=redefined-builtin
    apply(elements, _write,
            directory = directory,
            format = format,
            name_format=name_format)

clingo_json_schema = {
    "type": "object",
    "required": ["Call","Result"],
    "properties":{
        "Call": {
            "type" : "array",
        },
        "Result":{
            "type": "string",
        }
    }
}

def parse_clingo_json(json_str):
    """
    Parses a json string from the output of clingo obtained using the option ``--outf=2``.
    Expects a SATISFIABLE answer.

    Args:
        json_str (str): A string with the json

    Returns:
        (`list[str]`) A list with the programs as strings

    Raises:
        :py:class:`InvalidSyntax`: if the json format is invalid or is not a SAT result.
    """
    try:
        j = json.loads(json_str.encode())
        validate(instance=j, schema=clingo_json_schema)
        if j['Result'] == 'UNSATISFIABLE':
            log.warning("Passing an unsatisfiable instance in the JSON. This wont produce any results")

        if len(j["Call"]) > 1:
            log.warning("Calls will multiple theads from clingo are not supported by clingraph")

        if not "Witnesses" in j["Call"][0]:
            log.warning("No Witnesses (stable models) in the JSON output, no output will be produced by clingraph")
            witnesses = []
        else:
            witnesses = j["Call"][0]["Witnesses"]

        models_prgs = []
        for w in witnesses:
            prg_str = "\n".join([f"{v}." for v in w["Value"]])
            models_prgs.append(prg_str)

        return models_prgs

    except json.JSONDecodeError as e:
        raise InvalidSyntax('The json can not be read.',str(e)) from None
    except jsonschema.exceptions.ValidationError as e:
        raise InvalidSyntaxJSON('The json does not have the expected structure. Make sure you used the -outf=2 option in clingo.',str(e)) from None
