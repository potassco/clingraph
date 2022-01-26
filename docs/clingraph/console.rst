Console usage
#############

Clingraphs also comes with command line functionality.
Graphs can be from files or by a piping. 
The output will be the dot source code of the graphs defined by the input.
Graphs can also be rendered and saved with additional options for gif generation.

Special integration for `clingo <https://potassco.org/clingo/>`_ includes the creation of graphs for multiple stable models from a clingos’ json output format.

For advanced examples on how to use the command line see our `examples folder  <https://github.com/potassco/clingraph/tree/master/examples>`_. Each subfolder contains a README that explains how to run the example.

.. code:: shell

   clingraph --help

::

         _ _                         _
       __| (_)_ _  __ _ _ _ __ _ _ __| |_
     / _| | | ' \/ _` | '_/ _` | '_ \ ' \
     \__|_|_|_||_\__, |_| \__,_| .__/_||_|
                 |___/         |_|

     Clingraph is a package to generate graph visualizations
     based on facts that can be computed by logic programs.
     Special features for integration with clingo!


     positional arguments:
       files

     optional arguments:
       -h, --help            show this help message and exit
       -q                    Flag to have a quiet output where the graphs soruce wont be rendered
       -log                  Provide logging level.
                             {debug|info|error|warning}
                                 (default: warning)

     Graph generation:
       --type                The type of the graph: digraph or graph
                             {graph|digraph}
                                 (default: graph)
       --prefix              Prefix expected in all the considered facts
       --default-graph       The name of the default graph.
                             All nodes and edges with arity 1 will be assigned to this graph
                             (default: default)

     Graph rendering:
       --render              Flag to render the graphs and save in files
       --dir                 Directory for saving and rendering
                                 (default: out)
       --out-file-prefix     A prefix for the names of the generated files
                                 (default: )
       --format              Format to save the graph
                             {pdf|png|svg}
                                 (default: pdf)
       --engine              Layout command used by graphviz
                             {dot|neato|twopi|circo|fdp|osage|patchwork|sfdp}
                                 (default: dot)
       --view                Opens the generated files
       --select-graph  [ ...]
                             Select one of the graphs for output or rendering by name
                             Can appear multiple times to select multiple graphs
       --render-param [ ...]
                             A string containing a parameter for graphviz rendering.
                             String should have the form arg_name=arg_value
       --gif                 Flag to generate a giv from all the generated files
       --gif-name            Name for the gif file that will be saved in the given directory
       --gif-param [ ...]    A string containing a parameter for the gif generation by imageio.
                             String should have the form arg_name=arg_value

     Multi model graphs:
       --json                Flag to indicate the creation of multiple models from a json.
                             The graphs will be generated for each stable model.
                             The json is exptected to be the output of clingo using the option `--outf=2`
       --select-model []     Select only one of the models outputed by clingo defined by a number