"""
Clingraph functionality
"""
from ast import parse
import sys
import argparse
import textwrap
import pkg_resources

from .graphviz import compute_graphs, dot, render
from .logger import setup_logger_str, COLORS
from .orm import Factbase
from .utils import write, apply
from .exceptions import InvalidSyntaxJSON, InvalidSyntax
from .clingo_utils import _get_fbs_from_encoding, _get_json

try:
    VERSION = pkg_resources.require("clingraph")[0].version
except pkg_resources.DistributionNotFound:
    VERSION = '0.0.0'


__all__ = ["main"]

def _get_parser():
    """
    Get the parser for the command line
    """
    # pylint: disable=anomalous-backslash-in-string
    parser = argparse.ArgumentParser(description=textwrap.dedent("""
        _ _                         _
     __| (_)_ _  __ _ _ _ __ _ _ __| |_
    / _| | | ' \/ _` | '_/ _` | '_ \ ' \\
    \__|_|_|_||_\__, |_| \__,_| .__/_||_|
                |___/         |_|

    Clingraph is a package to generate graph visualizations
    based on facts that can be computed by logic programs.
    Special features for integration with clingo.
    """),
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('files',
        type=argparse.FileType('r'),
        help=textwrap.dedent('''\
            - Files containing facts that define the graph.
              See the allowed syntax: https://clingraph.readthedocs.io/en/latest/clingraph/syntax.html.

            - A single JSON file using clingos output option `--outf=2`.
            In this case, the facts defining the graphs will be loaded from each stable model.'''),
        nargs='*')
    parser.add_argument('stdin',
            type=argparse.FileType('r'),
            help=textwrap.dedent('''\
                Standard input in one of the following formats:
                    - A list of facts
                    - A json from clingos output option `--outf=2` '''),
            nargs='?',
            default=sys.stdin)
    parser.add_argument('-q',
                    help = """Flag to have a quiet output where the graphs source wont be rendered""",
                    action='store_true')
    parser.add_argument('-log', default="warning",
                    choices=['debug', 'info', 'error', 'warning'],
                    help=textwrap.dedent('''\
                        Provide logging level.
                        {debug|info|error|warning}
                            (default: %(default)s)'''),
                    type=str,
                    metavar='')
    parser.add_argument('--seed', default=None,
                help=textwrap.dedent('''\
                    Provide a seed for the outputs. It will be passed to clingo if viz-encoding in present,
                    and as the start attribute of the graphviz graphs https://graphviz.org/docs/attrs/start/'''),
                type=str,
                metavar='')
    parser.add_argument('--version','-v', action='version',
                    version=f'%(prog)s {VERSION}')


    input_params = parser.add_argument_group('INPUT', 'Options for the facts defining the graph.')
    input_params.add_argument('--prefix',
                    default = '',
                    help = textwrap.dedent('''\
                        Prefix expected in all the considered facts.
                        Example: --prefix=viz_ will look for predicates named viz_node, viz_edge etc.'''),
                    type=str,
                    metavar='')
    input_params.add_argument('--default-graph',
                    default = 'default',
                    help = textwrap.dedent('''\
                    The name of the default graph.
                    All nodes and edges with arity 1 will be assigned to this graph
                        (default: %(default)s)'''),
                    type=str,
                    metavar='')

    input_params.add_argument('--viz-encoding',
                    help = textwrap.dedent('''\
                        A visualization encoding that will be used to generate the graph facts
                        by calling clingo with the input.
                        This encoding is expected to have only one stable model.'''),
                    type=argparse.FileType('r'),
                    nargs='?',
                    metavar='')

    graphs_params = parser.add_argument_group('OUTPUT','Options to define the output.')

    graphs_params.add_argument('--out',
            default = 'facts',
            choices=['facts', 'dot', 'render', 'animate', 'tex'],
            help = textwrap.dedent('''\
                Type of output {facts|dot|render|animate|tex}
                    facts: The preprocessed facts
                    dot: The string in DOT language
                    render: Generates images with the rendering method of graphviz
                    animate: Generates an animation in gif format after rendering
                    tex: Generates a latex file
                    (default: %(default)s)
                See below for additional special options for each output type.
                -'''),
            type=str,
            metavar="")

    graphs_params.add_argument('--select-graph',
            help = textwrap.dedent('''\
                Select one of the graphs by name.
                Can appear multiple times to select multiple graphs'''),
            type=str,
            action='append',
            nargs='?',
            metavar="")

    graphs_params.add_argument('--select-model',
            help = textwrap.dedent('''\
                Select only one of the models when using a json input.
                Defined by a number starting in index 0.
                Can appear multiple times to select multiple models.'''),
            type=int,
            action='append',
            nargs='?',
            metavar="")

    graphs_params.add_argument('--name-format',
                help = textwrap.dedent('''\
                    An optional string to format the name when saving multiple files,
                    this string can reference parameters `{graph_name}` and `{model_number}`.
                    Example `new_version-{graph_name}-{model_number}`
                    (default: `{graph_name}` or
                              `{model_number}/{graph_name}` for multi model functionality from json)'''),
                type=str,
                metavar='')


    graphs_params.add_argument('--dir',
                    default = 'out',
                    help = textwrap.dedent('''\
                        Directory for writing the output files
                            (default: %(default)s)'''),
                    type=str,
                    metavar='')

    graphs_params.add_argument('--save',
                action='store_true',
                help = textwrap.dedent('''\
                    Saves the output in files based on the directory, name format and fortmat provided.
                    Otherwise the output is just printed on the stdout'''))

    graphviz_params = parser.add_argument_group('OUTPUT {dot|render|tex|animate}','Options for the functionality regarding graphviz.')


    graphviz_params.add_argument('--type',
                default = 'graph',
                choices=['graph', 'digraph'],
                help = textwrap.dedent('''\
                    The type of the graph
                    {graph|digraph}
                        (default: %(default)s)'''),
                type=str,
                metavar='')

    graphviz_params.add_argument('--engine',
                    default = 'dot',
                    choices=["dot","neato","twopi","circo","fdp","osage","patchwork","sfdp"],
                    help = textwrap.dedent('''\
                        Layout command used by graphviz
                        {dot|neato|twopi|circo|fdp|osage|patchwork|sfdp}
                            (default: %(default)s)'''),
                    type=str,
                    metavar="")


    graphviz_render_params = parser.add_argument_group('OUTPUT {render}', 'Options to render graphviz objects.')


    graphviz_render_params.add_argument('--format',
                    default = 'pdf',
                    choices=['pdf', 'png', 'svg'],
                    help = textwrap.dedent('''\
                        Format to save the graph
                        {pdf|png|svg}
                            (default: %(default)s)'''),
                    type=str,
                    metavar="")

    graphviz_render_params.add_argument('--view',
                action='store_true',
                help = textwrap.dedent('''\
                    Opens the generated files'''))


    graphviz_gif_params = parser.add_argument_group('OUTPUT {animate}','Options for the animation')

    graphviz_gif_params.add_argument('--fps',
                default = 1,
                help = textwrap.dedent('''\
                The number of frames per second.
                    (default: %(default)s)'''),
                type=float,
                metavar='')

    graphviz_gif_params.add_argument('--sort',
            default = 'asc-str',
            help = textwrap.dedent('''\
            How to sort the images used to generate the gif
                asc-str: Sort ascendent based on the graph name as a string
                asc-int: Sort ascendent based on the graph name converted to an integer
                desc-str: Sort descendent based on the graph name as a string
                desc-int: Sort descendent based on the graph name converted to an integer
                name1,...,namex: A string with the order of the graph names separated by `,`
                (default: %(default)s)'''),
            type=str,
            metavar='')

    graphviz_tex_params = parser.add_argument_group('OUTPUT {tex}', 'Options for the generation of latex files')


    graphviz_tex_params.add_argument('--tex-param',
                default = '',
                help = textwrap.dedent('''\
                A string containing a parameter for the tex file generation by dot2tex.
                String should have the form arg_name=arg_value for a valid option:
                    https://dot2tex.readthedocs.io/en/latest/usage_guide.html '''),
                type=str,
                nargs='*',
                metavar='')

    return parser

def _get_fbs_normal(args,stdin,prgs_from_json):
    fbs = []
    if prgs_from_json is not None:
        fbs = [Factbase.from_string(prg,prefix=args.prefix,
                                        default_graph=args.default_graph)
                for prg in prgs_from_json]
    else:
        fb= Factbase(prefix=args.prefix,default_graph=args.default_graph)
        fb.add_fact_string(stdin)
        for f in args.files:
            fb.add_fact_file(f.name)
        fbs = [fb]

    return fbs

def main():
    '''
    Runs the main function
    '''
    #pylint:disable=too-many-branches
    ####### Parser
    parser= _get_parser()
    args = parser.parse_args()

    ####### Logger
    log = setup_logger_str(args.log)

    log.debug(args)

    ####### READ stdin
    stdin = ""
    if not sys.stdin.isatty():
        stdin = parser.parse_args().stdin.read()

    ######## LOAD Fact base
    fbs = []
    prg_from_json = _get_json(args,stdin)
    if args.viz_encoding:
        fbs = _get_fbs_from_encoding(args,stdin,prg_from_json)
    else:
        fbs = _get_fbs_normal(args,stdin,prg_from_json)

    log.debug(fbs)
    ######## Name format
    if prg_from_json:
        if args.name_format is None:
            args.name_format = '{model_number}/{graph_name}'
    else:
        if args.name_format is None:
            args.name_format = '{graph_name}'

    ######## Model selection
    if args.select_model is not None:
        for m in args.select_model:
            if m>=len(fbs):
                raise ValueError(f"Invalid model number selected {m}")
        fbs = [f if i in args.select_model else None
                    for i, f in enumerate(fbs) ]


    ######## Warnings
    n_models = len([f for f in fbs if f is not None])
    if n_models>1 and not args.q and not args.save and not (args.out in ['render','animate']):
        log.warning("Outputing multiple models in stdout.")
    if n_models>1 and not '{model_number}' in args.name_format:
        log.warning("Output files will be overwritten since no `{model_number}` is used in the name format argument.")

    write_arguments = {"directory":args.dir, "name_format":args.name_format}

    ######## OUT=facts
    if args.out == 'facts':
        log.debug("Log option facts")
        fbs_as_elements = [{'graphviz_facts':str(f)} for f in fbs]
        if args.save:
            write(fbs_as_elements,format = 'lp',**write_arguments)
        else:
            apply(fbs_as_elements,print)
        sys.exit()

    ######## Compute graphs
    graphs = compute_graphs(fbs,graphviz_type=args.type,seed=args.seed)
    if args.select_graph is not None:
        graphs = [{g_name:g for g_name, g in graph.items() if g_name in args.select_graph}
                    for graph in graphs]

    def out_str(t, g_name, p):
        s = f"{COLORS['BLUE']}->{COLORS['NORMAL']} {t} for graph {COLORS['YELLOW']}{g_name}{COLORS['NORMAL']},"
        return s + f" saved in: {COLORS['BLUE']}{p}{COLORS['NORMAL']}"
    ######## OUT=dot
    if args.out == 'dot':
        log.debug("Out option: dot")
        dots = dot(graphs)
        if args.save:
            write(dots,format='dot',**write_arguments)
        else:
            apply(dots,print)
        sys.exit()

    ######## OUT=render
    if args.out == 'render':
        log.debug("Out option: render")
        paths = render(graphs,
                format=args.format,
                engine=args.engine,
                view=args.view,
                **write_arguments)
        if not args.q:
            for p_dic in paths:
                if p_dic is None:
                    continue
                for g_name, p in p_dic.items():
                    print(out_str("Image",g_name,p))
        sys.exit()

    ######## OUT=tex
    if args.out == 'tex':
        #pylint: disable=import-outside-toplevel
        from .tex import tex
        log.debug("Out option: tex")
        tex_params = []
        if args.tex_param is not None:
            tex_params = args.tex_param
        tex_param_dic = { s.split('=')[0]:s.split('=')[1] for s in tex_params}

        texs = tex(graphs,**tex_param_dic)
        if args.save:
            paths = write(texs,format='tex',**write_arguments)
            if not args.q:
                for p_dic in paths:
                    if p_dic is None:
                        continue
                    for g_name, p in p_dic.items():
                        print(out_str("File",g_name,p))

        else:
            apply(texs,print)
        sys.exit()

    ######## OUT=gif
    if args.out == 'animate':
        #pylint: disable=import-outside-toplevel
        from .gif import save_gif
        log.debug("Out option: animate")
        paths = save_gif(graphs,
                engine=args.engine,
                fps = args.fps,
                sort=args.sort,
                **write_arguments)
        if not args.q:
            for p_dic in paths:
                if p_dic is None:
                    continue
                for g_name, p in p_dic.items():
                    print(out_str("Gif",g_name,p))


        sys.exit()
