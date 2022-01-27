Command line functionality
##########################

Clingraph also comes with command line functionality.
The graphs can be generated from files or by a piping some output.
Then, clingraph will output be the source dot code of the graphs defined by the input.
Graphs can also be rendered and saved, with additional options for gif generation.

Special integration for `clingo <https://potassco.org/clingo/>`_ includes the creation of graphs for multiple stable models from a clingos’ json output format.

.. note:: For advanced examples on how to use the command line see our `examples folder  <https://github.com/potassco/clingraph/tree/master/examples>`_. Each subfolder contains a README that explains how to run the example.

.. code:: shell

   $ clingraph --help

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


Basic example
=============

Loading facts from a file with a single graph
----------------------------------------------

- The file to load which contains only facts.

.. code:: shell

  $ cat examples/basic/example3/example_3.lp

*Output:*

.. code:: shell

    graph(house).
    graph(bathroom, house).
    graph(bedroom, house).

    node(toilet,bathroom).
    node(bed,bedroom).
    node(desk,bedroom).

    edge((toilet,bed),house).


    attr(graph, house, label, "Tom's House").
    attr(graph, bathroom, style, dotted).
    attr(graph, bathroom, label, "Bathroom").
    attr(graph, bedroom, style, dotted).
    attr(graph, bedroom, label, "Bedroom").

    attr(graph_nodes, house, style, filled).
    attr(graph_nodes, house, color, cyan).

    attr(node, toilet, shape, circle).
    attr(node, bed, shape, square).
    attr(node, desk, shape, square).

    attr(edge, (toilet,bed), color, red).



- Run clingraph to obtain the graphviz representation.

.. code:: shell

  $ clingraph examples/basic/example3/example_3.lp

*Output:*

.. code:: shell

   //----------house----------
  graph house {
    graph [label="Tom's House"]
    node [color=cyan style=filled]
    toilet -- bed [color=red]
    subgraph cluster_bathroom {
      graph [label=Bathroom style=dotted]
      toilet [shape=circle]
    }
    subgraph cluster_bedroom {
      graph [label=Bedroom style=dotted]
      bed [shape=square]
      desk [shape=square]
    }
  }


Loading facts from a piped output with multiple graphs
------------------------------------------------------

- The file which contains only facts.

.. code:: shell

  $ cat examples/basic/example2/example_2.lp

*Output:*

.. code:: shell

    graph(toms_family).
    graph(bills_family).

    node(tom, toms_family).
    node(max, toms_family).
    edge((tom, max), toms_family).

    node(bill, bills_family).
    node(jen, bills_family).
    edge((bill, jen), bills_family).


- Run clingraph to obtain the graphviz representation.

.. code:: shell

  $ cat examples/basic/example2/example_2.lp | clingraph

*Output:*

.. code:: shell
    
    //----------toms_family----------
    graph toms_family {
      tom
      max
      tom -- max
    }
    //----------bills_family----------
    graph bills_family {
      bill
      jen
      bill -- jen
    }


- Select only one graph from output

.. code:: shell

  $ cat examples/basic/example2/example_2.lp | clingraph --select-graph=toms_family

*Output:*

.. code:: shell
    
    //----------toms_family----------
    graph toms_family {
      tom
      max
      tom -- max
    }

- Render the graphviz and save it in a directory

.. code:: shell

  $ cat examples/basic/example2/example_2.lp | clingraph --select-graph=toms_family --render --format=pdf --dir='out' -log=info

*Output:*

.. code:: shell
    
    INFO:  - Image saved in out/toms_family.pdf
    //----------toms_family----------
    graph toms_family {
      tom
      max
      tom -- max
    }


Clingo integration
==================

- The clingo program written by the user. Note that the choice will account to multiple stable models.
  
.. code:: shell

  $ cat examples/basic/example5/example_5.lp

*Output:*

.. code:: shell
    
  1{node(a);node(b)}1.

  attr(node,a,color,blue):-node(a).
  attr(node,b,color,red):-node(b).

- Run clingo to obtain the json output with option ``--outf=2```

.. code:: shell

  $ clingo examples/basic/example5/example_5.lp -n 0 --outf=2

*Output:*

.. code:: shell
    
  {
    "Solver": "clingo version 5.5.0",
    "Input": [
      "examples/basic/example5/example_5.lp"
    ],
    "Call": [
      {
        "Witnesses": [
          {
            "Value": [
              "attr(node,a,color,blue)", "node(a)"
            ]
          },
          {
            "Value": [
              "attr(node,b,color,red)", "node(b)"
            ]
          }
        ]
      }
    ],
    "Result": "SATISFIABLE",
    "Models": {
      "Number": 2,
      "More": "no"
    },
    "Calls": 1,
    "Time": {
      "Total": 0.001,
      "Solve": 0.000,
      "Model": 0.000,
      "Unsat": 0.000,
      "CPU": 0.001
    }
  }


- Pipe clingos json to clingraph with the ``--json`` option

.. code:: shell

  $ clingo examples/basic/example5/example_5.lp -n 0 --outf=2 | clingraph --json

*Output:*

.. code:: shell
    
  //=========================
  //	Model: 1 Costs: []
  //=========================

  //----------default----------
  graph default {
    a [color=blue]
  }

  //=========================
  //	Model: 2 Costs: []
  //=========================

  //----------default----------
  graph default {
    b [color=red]
  }



- Select one of the models by number and save it

.. code:: shell

  $ clingo examples/basic/example5/example_5.lp -n 0 --outf=2 | clingraph --json --select-model=1 --render --format=png -log=info

*Output:*

.. code:: shell
    
  INFO:  - Loading a multi model graph from json
  INFO:  - Image saved in out/default.png
  //----------default----------
  graph default {
    a [color=blue]
  }
