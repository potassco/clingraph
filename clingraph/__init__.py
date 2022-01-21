from ast import parse
import sys
from clingraph.graph import Clingraph
import logging
import argparse, textwrap
from clingraph.logger import setup_logger

def get_parser():
    parser = argparse.ArgumentParser(description="""
     _ _                         _    
  __| (_)_ _  __ _ _ _ __ _ _ __| |_  
 / _| | | ' \/ _` | '_/ _` | '_ \ ' \ 
 \__|_|_|_||_\__, |_| \__,_| .__/_||_|
             |___/         |_|        

Clingraph is a package to generate graph visualizations 
based on facts that can be computed by logic programs.
Special features for integration with clingo.
    """,
    formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('files', type=argparse.FileType('r'), nargs='+')
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
                        Can apear multiple times to select multiple graphs'''),
                    type=str,
                    nargs='+',
                    metavar="")

    render_params.add_argument('--render-params',
                    default = '',
                    help = textwrap.dedent('''\
                    A string containing parameters for the graphviz rendering.
                    Must be pairs of key values separated by a space.
                    Example: key1:value1 key2:value2'''),
                    type=str,
                    metavar='')

    render_params.add_argument('--gif', 
                    help = """Flag to generate a giv from all the generated files""",
                    action='store_true')

    render_params.add_argument('--gif-name',
                default = 'clingraph',
                help = textwrap.dedent('''\
                Name for the gif file that will be saved in the given directory'''),
                type=str,
                metavar='')

    render_params.add_argument('--gif-params',
                default = '',
                help = textwrap.dedent('''\
                A string containing parameters for the gif generation by imageio.
                Must be pairs of key values separated by a space.
                Example: key1:value1 key2:value2'''),
                type=str,
                metavar='')


    parser.add_argument('--json', action='store_true')

    return parser

def main():
    '''
    Runs the main function
    '''
    ####### Parser
    parser= get_parser()
    args = parser.parse_args()
    
    ####### Logger
    LOG = logging.getLogger('custom')
    levels = {'error': logging.ERROR, 'warn': logging.WARNING,
              'warning': logging.WARNING, 'info': logging.INFO, 'debug': logging.DEBUG}
    setup_logger(levels.get(args.log.lower()))

    ####### Load input
    input_str = sys.stdin.read()
    if args.json:
        LOG.info(f"Create multiple model graphs from json")
        
        
    g = Clingraph(type_ = args.type, prefix=args.prefix, default_graph=args.default_graph)

    for f in args.files:
        LOG.info(f"Adding file {f.name}")
        g.add_fact_file(f.name)

    if input_str:
        g.add_fact_string(input_str)

    g.compute_graphs()

    ####### Output

    if args.render:
        g.save(args.dir,format=args.format,name_prefix=args.out_file_prefix,selected_graphs=args.select_graph)
    if args.gif:
        g.save_gif(args.dir,name=args.gif_name,engine=args.engine,selected_graphs=args.select_graph)
    
    if not args.q:
        if args.select_graph:
            for g_name in args.select_graph:
                print(g.graphs[g_name])
        else:
            print(g)

