"""
Functions used for the clingo integration
"""

import json
import logging
import jsonschema
from clingo.control import Control
from clingo.script import enable_python
from clingo.symbol import String
from jsonschema import validate
from .orm import Factbase
from .exceptions import InvalidSyntaxJSON, InvalidSyntax

enable_python()
log = logging.getLogger('custom')

class ClingraphContext:
    """
    Provides avaliable python functions to be used in a visualization encoding
    passed in the command line via option `--viz-encoding`
    """

    def pos(self, x,y):
        """
        Args:
            x (clingo.Symbol.Number): Number for the X coordinate
            y (clingo.Symbol.Number): Number for the Y coordinate
        Returns:
            (clingo.Symbol.String) position as a string of form (x,y)!
        """

        return String(f"{str(x)},{str(y)}!")

    def concat(self, *args):
        """
        Concatenates the given symbols as a string
        Args:
            args: All symbols
        Returns:
            (clingo.Symbol.String) The string concatenating all symbols
        """
        return String(''.join([str(x).strip('"') for x in args]))

    def __getattr__(self, name):
        # pylint: disable=import-outside-toplevel

        import __main__
        return getattr(__main__, name)


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



def _get_json(args, stdin):
    """
    Gets the json from the arguments, in case one is provided
    """
    json_str = None

    for f in args.files:
        if ".json" not in f.name:
            return None
        if json_str is not None:
            raise ValueError("Only one json file can be provided")
        json_str = f.read()
    try:
        prg_list = parse_clingo_json(stdin)
        if json_str is not None:
            raise ValueError("Only one json can be provided as input.")
        return prg_list
    except InvalidSyntaxJSON as e:
        raise e from None
    except InvalidSyntax:
        if json_str is None:
            return None
        try:
            prg_list = parse_clingo_json(json_str)
            return prg_list
        except InvalidSyntaxJSON as e:
            raise e from None
        except InvalidSyntax as e:
            return None


def _get_fbs_from_encoding(args,stdin,prgs_from_json):
    """
    Obtains the factbase by running clingo to compute the stable models
    of a visualization encoding
    """
    fbs = []
    def add_fb_model(m):
        fbs.append(Factbase.from_model(m,
                    prefix=args.prefix,
                    default_graph=args.default_graph))

    cl_args = ["-n1"]
    if args.seed is not None:
        cl_args.append(f'--seed={args.seed}')
    if prgs_from_json is not None:
        for prg in prgs_from_json:
            ctl = Control(cl_args)
            ctl.load(args.viz_encoding.name)
            ctl.add("base",[],prg)
            ctl.ground([("base", [])],ClingraphContext())
            ctl.solve(on_model=add_fb_model)
    else:
        ctl = Control(cl_args)
        ctl.load(args.viz_encoding.name)
        ctl.add("base",[],stdin)
        for f in args.files:
            ctl.load(f.name)
        ctl.ground([("base", [])],ClingraphContext())
        ctl.solve(on_model=add_fb_model)

    return fbs
