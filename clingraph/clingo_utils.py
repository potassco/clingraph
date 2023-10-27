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

    def pos(self, x,y,scale=1):
        """
        Args:
            x (clingo.Symbol.Number): Number for the X coordinate
            y (clingo.Symbol.Number): Number for the Y coordinate
        Returns:
            (clingo.Symbol.String) position as a string of form (x,y)!
        """
        scale = float(str(scale).strip('"'))
        x = float(str(x))*scale
        y = float(str(y))*scale
        return String(f"{x},{y}!")

    def concat(self, *args):
        """
        Concatenates the given symbols as a string
        Args:
            args: All symbols
        Returns:
            (clingo.Symbol.String) The string concatenating all symbols
        """
        return String(''.join([str(x).strip('"') for x in args]))

    def format(self, s, *args):
        """
        Formats the string with the given arguments
        Args:
            s (clingo.Symbol.String): The string to format, for example "{0} and {1}"
            args: All symbols that can be accessed by the position starting in 0
        Returns:
            (clingo.Symbol.String) The string concatenating all symbols
        """
        args_str = [str(v).strip('"') for v in args]
        return String(s.string.format(*args_str))

    def stringify(self, s, capitalize=False):
        """
        Turns a value into a string without underscore and capitalized if requested
        Args:
            s: The value to transform
        Returns:
            (clingo.Symbol.String) The string
        """
        val = str(s).strip('"')
        val = val.replace('_',' ')
        if capitalize:
            val = val[0].upper() + val[1:]
        return String(val)

    def cluster(self, s):
        """
        Returns the cluster name for a graph
        Args:
            s: The identifier of the graph
        Returns:
            (clingo.Symbol.String) The string with the cluster name
        """
        val = str(s).strip('"')
        return String("cluster_"+val)


    def html_escape(self, s):
        """
        Will escape the symbols of an HTML-Like label that provoque clashes: &, < and >
        Args:
            s (clingo.Symbol): The value that needs the symbols removed
        Returns:
            (clingo.Symbol.String) The string with the replacements
        """

        return String(
            str(s).strip('"')
                .replace('&', '&amp;')
                .replace('"', '&quot;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

    def svg_init(self, property_name, property_value):
        """
        Generates an svg string for the initial state. This string has a format that is handled
        by clingraph internally in the generation of svg files. This property will be set on the
        group tag `<g>` used around the elements. Notice that any properties set using the `attr`
        predicates will not be overwritten.

        Args:
            property_name: The name of the css property to set.
            property_value: The value of the property to set
        Returns:
            (clingo.Symbol.String) The string representing the property
        """
        property_name = str(property_name).strip('"')
        property_value = str(property_value).strip('"')
        return String(f"init___{property_name}___{property_value} ")

    def svg_color(self):
        """
        Generates an svg string that is used as a placeholder for the color in properties.
        This string will be mapped into the css variable `currentcolor`.
        Returns:
            (clingo.Symbol.String) The string as a color placeholder
        """
        return String("#111111")

    def svg(self, event, element, property_name, property_value):
        """
        Generates an svg string for interactive actions This property will be set on the group tag
        `<g>` used around the elements. Notice that any properties set using the `attr` predicates
        will not be overwritten.
        Args:
            event: The svg event one of: "click","mouseenter","mouseleave","contextmenu"
            element: The id on the element in which the action is performed. This element must have the id property set: `attr(node,ID,id,ID):-node(ID).`
            property_name: The name of the css property to set.
            property_value: The value of the property to set
        Returns:
            (clingo.Symbol.String) The string internal representation of the interaction
        """
        event = str(event).strip('"')
        element = str(element).strip('"')
        property_name = str(property_name).strip('"')
        property_value = str(property_value).strip('"')
        s=String(f"{event}___{element}___{property_name}___{property_value} ")
        return s

    def color(self, option, opacity=None):
        """
        Gets the html color code for the different options and the given opacity
        Args:
            option: primary, secondary, success, info, warning, danger, light
            opacity: Numeric value indicating the opacity of the color
        """
        option = str(option)
        opacity = str(opacity) if opacity is not None else None
        colors = {
            "primary": "#0052CC",
            "blue": "#0052CC",
            "secondary": "#6554C0",
            "purple": "#6554C0",
            "success": "#36B37E",
            "green": "#36B37E",
            "info": "#B3BAC5",
            "gray": "#B3BAC5",
            "warning": "#FFAB00",
            "yellow": "#FFAB00",
            "danger": "#FF5630",
            "red": "#FF5630",
            "light": "#F4F5F7"
        }
        if option not in colors:
            return String("#000000")

        hex_color = colors[option]

        if opacity is not None and opacity.isnumeric():
            o = int(opacity)
            if 0 <= o < 100:
                hex_color = f"{hex_color}{o:02d}"
        return String(hex_color)

    def clinguin_fontname(self):
        """
        Gets the font name used in clinguin
        """

        return String("Helvetica Neue")



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


SVG_SCRIPT = """
<script>
      <script type="text/javascript">

        var edges = Object.values(document.getElementsByClassName('edge'));
        var nodes = Object.values(document.getElementsByClassName('node'));
        var elements = edges.concat(nodes);
        const events = ["click","mouseenter","mouseleave","contextmenu"];
        window.onload=function(){
            elements.forEach(elem => {
                elem.classList.forEach(c => {
                    c_vals = c.split('___')
                    if (c_vals[0] == 'init'){
                        property = c_vals[1]
                        property_val = c_vals[2]
                        elem.style[property]=property_val
                    }
                    if (events.includes(c_vals[0])){
                        elem.classList.add(c_vals[0]+"_"+c_vals[1])
                    }
                })
            })
            elements.forEach(elem => {
                elem.addEventListener("contextmenu", e => e.preventDefault());
                events.forEach(event => {
                    elem.addEventListener(event, function() {
                        console.log(event)
                        local_event = event;
                        class_name = local_event + "_" + elem.id;
                        var children = Object.values(document.getElementsByClassName(class_name));
                        children.forEach(c => {
                            c.classList.forEach(c_elem =>{
                                c_vals = c_elem.split('___')
                                if (c_vals.length == 4){
                                    if (c_vals[0]==local_event){
                                        if(c_vals[1]==elem.id){
                                            property = c_vals[2]
                                            property_val = c_vals[3]
                                            c.style[property]=property_val
                                        }
                                    }
                                }
                            })
                        })


                    })
                })
            });
        }
      </script>

</script>
</svg>
"""

def add_svg_interaction_to_string(s):
    """
    Adds the svg interaction script to string representation of the svg image

    Args:
        s [str]: the svg string
    """
    s = s.replace("#111111","currentcolor")
    s = s[:-8]
    s+= SVG_SCRIPT
    return s

def add_svg_interaction(paths):
    """
    Adds the svg interaction script to a list of svg files defined in the paths.
    This paths can be the output of the render function.

    Args:
        paths [dic | list[dic]]: A dictionary with the paths where the images where saved as values for each graph.
        Or a list of such dictionaries, each element corresponding to a model.
    """
    for path_dic in paths:
        if not path_dic:
            continue
        for path in path_dic.values():
            with open(path, 'r', encoding='UTF-8') as f:
                s = f.read()
                s = add_svg_interaction_to_string(s)
            with open(path, 'w', encoding='UTF-8') as f:
                f.write(s)

ADD_IDS_PRG = """
#defined edge/2.
#defined edge/1.
#defined node/1.
#defined node/2.
#defined graph/1.
#defined graph/2.
attr(node,ID,id,ID):-node(ID).
attr(node,ID,id,ID):-node(ID,_).
attr(edge,ID,id,ID):-edge(ID).
attr(edge,ID,id,ID):-edge(ID,_).
attr(graph,ID,id,ID):-graph(ID).
attr(graph,ID,id,ID):-graph(ID,_).
"""

def add_elements_ids(ctl):
    """
    Adds a program to the control that will set the ids of the elements to the id attribute
    Args:
        ctl Clingo.Control: The clingo control object that is used
    """

    ctl.add("base",[],ADD_IDS_PRG)


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
            if args.format == 'svg':
                add_elements_ids(ctl)
            ctl.ground([("base", [])],ClingraphContext())
            ctl.solve(on_model=add_fb_model)
    else:
        ctl = Control(cl_args)
        ctl.load(args.viz_encoding.name)
        ctl.add("base",[],stdin)
        if args.format == 'svg':
            add_elements_ids(ctl)
        for f in args.files:
            ctl.load(f.name)
        ctl.ground([("base", [])],ClingraphContext())
        ctl.solve(on_model=add_fb_model)

    return fbs
