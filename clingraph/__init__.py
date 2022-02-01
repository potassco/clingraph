"""
    Package inports and command line functionality
"""
from ast import parse
import sys
import logging
import argparse
import textwrap
import pkg_resources
from clingraph.clingraph import Clingraph
from clingraph.logger import setup_logger
from clingraph.multigraph import MultiModelClingraph
from clingraph.orm import ClingraphORM
from clingraph.exception import InvalidSyntax
version = pkg_resources.require("clingraph")[0].version

def get_parser():
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
    parser.add_argument('files', type=argparse.FileType('r'), nargs='*')
    parser.add_argument('-q',
                    help = """Flag to have a quiet output where the graphs soruce wont be rendered""",
                    action='store_true')
    parser.add_argument('-log', default="warning",
                    choices=['debug', 'info', 'error', 'warning'],
                    help=textwrap.dedent('''\
                        Provide logging level.
                        {debug|info|error|warning}
                            (default: %(default)s)'''),
                    type=str,
                    metavar='')
    parser.add_argument('--version','-v', action='version',
                    version=f'%(prog)s {version}')


    input_params = parser.add_argument_group('Graph generation')
    input_params.add_argument('--type',
                    default = 'graph',
                    choices=['graph', 'digraph'],
                    help = textwrap.dedent('''\
                        The type of the graph: digraph or graph
                        {graph|digraph}
                            (default: %(default)s)'''),
                    type=str,
                    metavar='')
    input_params.add_argument('--prefix',
                    default = '',
                    help = textwrap.dedent('''\
                        Prefix expected in all the considered facts'''),
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

    render_params = parser.add_argument_group('Graph rendering')
    render_params.add_argument('--render',
                    help = """Flag to render the graphs and save in files""",
                    action='store_true')

    render_params.add_argument('--dir',
                    default = 'out',
                    help = textwrap.dedent('''\
                        Directory for saving and rendering
                            (default: %(default)s)'''),
                    type=str,
                    metavar='')

    render_params.add_argument('--out-file-prefix',
                    default = '',
                    help = textwrap.dedent('''\
                        A prefix for the names of the generated files
                            (default: %(default)s)'''),
                    type=str,
                    metavar='')

    render_params.add_argument('--format',
                    default = 'pdf',
                    choices=['pdf', 'png', 'svg'],
                    help = textwrap.dedent('''\
                        Format to save the graph
                        {pdf|png|svg}
                            (default: %(default)s)'''),
                    type=str,
                    metavar="")
    render_params.add_argument('--engine',
                    default = 'dot',
                    choices=["dot","neato","twopi","circo","fdp","osage","patchwork","sfdp"],
                    help = textwrap.dedent('''\
                        Layout command used by graphviz
                        {dot|neato|twopi|circo|fdp|osage|patchwork|sfdp}
                            (default: %(default)s)'''),
                    type=str,
                    metavar="")

    render_params.add_argument('--view',
                action='store_true',
                help = textwrap.dedent('''\
                    Opens the generated files'''))

    render_params.add_argument('--select-graph',
                    help = textwrap.dedent('''\
                        Select one of the graphs for output or rendering by name
                        Can appear multiple times to select multiple graphs'''),
                    type=str,
                    nargs='+',
                    metavar="")

    render_params.add_argument('--render-param',
                    default = '',
                    help = textwrap.dedent('''\
                    A string containing a parameter for graphviz rendering.
                    String should have the form arg_name=arg_value '''),
                    type=str,
                    nargs='*',
                    metavar='')

    render_params.add_argument('--gif',
                    help = """Flag to generate a gif from all the generated files""",
                    action='store_true')

    render_params.add_argument('--gif-name',
                default = 'clingraph',
                help = textwrap.dedent('''\
                Name for the gif file that will be saved in the given directory'''),
                type=str,
                metavar='')

    render_params.add_argument('--gif-param',
                default = '',
                help = textwrap.dedent('''\
                A string containing a parameter for the gif generation by imageio.
                String should have the form arg_name=arg_value '''),
                type=str,
                nargs='*',
                metavar='')


    render_params.add_argument('--tex',
                    help = """Flag to generate a latex tex file""",
                    action='store_true')

    render_params.add_argument('--tex-param',
                default = '',
                help = textwrap.dedent('''\
                A string containing a parameter for the tex file generation by dot2tex.
                String should have the form arg_name=arg_value '''),
                type=str,
                nargs='*',
                metavar='')

    multi_params = parser.add_argument_group('Multi model graphs')

    multi_params.add_argument('--json',
                help = textwrap.dedent('''\
                Flag to indicate the creation of multiple models from a json.
                The graphs will be generated for each stable model.
                The json is exptected to be the output of clingo using the option `--outf=2`'''),
                action='store_true')

    multi_params.add_argument('--select-model',
                help = textwrap.dedent('''\
                    Select only one of the models outputed by clingo defined by a number'''),
                type=int,
                nargs='?',
                metavar="")
    return parser

def setup_clingraph_log(log_str):
    '''
    Setup the clingraph log to get given level
    '''
    ####### Logger
    log = logging.getLogger('custom')
    levels = {'error': logging.ERROR, 'warn': logging.WARNING,
              'warning': logging.WARNING, 'info': logging.INFO, 'debug': logging.DEBUG}
    setup_logger(levels.get(log_str.lower()))
    log.debug("Log level set to %s",log_str)
    return log

def main():
    '''
    Runs the main function
    '''
    ####### Parser
    parser= get_parser()
    args = parser.parse_args()

    ####### Logger
    log = setup_clingraph_log(args.log)

    log.debug(args)
    ####### Load input
    input_str=""
    if not sys.stdin.isatty():
        input_str = sys.stdin.read()

    g = None
    if not args.json:
        g = Clingraph(type_ = args.type, prefix=args.prefix, default_graph=args.default_graph)

        for f in args.files:
            log.info("Adding file %s",f.name)
            g.add_fact_file(f.name)

        if input_str:
            g.add_fact_string(input_str)

    else:
        log.info("Loading a multi model graph from json")

        g = MultiModelClingraph(type_ = args.type, prefix=args.prefix, default_graph=args.default_graph)

        g.load_json(input_str)

    g.compute_graphs()

    ####### Output
    if not args.select_model is None and args.json:
        g=g.get_clingraph(args.select_model)

    if args.render:
        render_params = []
        if args.render_param is not None:
            render_params = args.render_param
        render_param_dic = { s.split('=')[0]:s.split('=')[1] for s in render_params}
        g.save(directory=args.dir,format=args.format,name_prefix=args.out_file_prefix,
            selected_graphs=args.select_graph,
            view=args.view, engine=args.engine,
            **render_param_dic)
    if args.gif:
        gif_params = []
        if args.gif_param is not None:
            gif_params = args.gif_param
        gif_param_dic = { s.split('=')[0]:s.split('=')[1] for s in gif_params}

        g.save_gif(directory=args.dir,name=args.gif_name,
            engine=args.engine,
            selected_graphs=args.select_graph, **gif_param_dic)

    if args.tex:
        tex_params = []
        if args.tex_param is not None:
            tex_params = args.tex_param
        tex_param_dic = { s.split('=')[0]:s.split('=')[1] for s in tex_params}

        g.save_tex(directory=args.dir,
            selected_graphs=args.select_graph, **tex_param_dic)

    if not args.q:
        print(g.source(args.select_graph))
