Command line functionality
##########################

Clingraph provides command line functionality to generate graphs from files and standard input.
The graphs can then be printed as a dot string, rendered, converted into a gif or into latex code.

Special integration for `clingo <https://potassco.org/clingo/>`_ includes the creation of graphs from multiple stable models using clingos’ json output format.

.. note:: 
  For advanced examples on how to use the command line see our `examples folder  <https://github.com/potassco/clingraph/tree/master/examples>`_. 
  Each subfolder contains a README explaining how to run the example.

The command line usage is described below. However, the latest available options can be found by running:

.. code:: shell

   $ clingraph --help


Loading facts
=============

The input can be loaded from multiple files and standard input, following our :ref:`syntax <syntax>`.
Any additional predicates will be ignored.
Additionally, a single JSON file can be provided instead, with the structure of clingos json output format with `--outf=2`. More details can be found in :ref:`clingo integration<Clingo integration>`

Consider the file `example1.lp <https://github.com/potassco/clingraph/blob/master/examples/doc/example1/example1.lp>`_

.. include:: ../../examples/doc/example1/example1.lp
  :literal:


- **Load from a file**

.. code:: shell

  $ clingraph example1.lp

- **Load from from stdin**

.. code:: shell

  $ cat example1.lp | clingraph

.. code:: shell

  node(john,default).
  node(jane,default).
  attr(node,jane,(label,-1),"Jane Doe").
  attr(node,john,(label,-1),"John Doe").
  attr(graph,default,(label,-1),"Does family").
  attr(graph_nodes,default,(style,-1),filled).
  edge((john,jane),default).
  graph(default). 

  
Output
======

Output formats
++++++++++++++

Clingraph provides four types of outputs
  - ``facts``: Shows all the facts provided that are part of the syntax, after preprocessing
  - ``dot``: Generates the graphviz objects and prints the source DOT language
  - ``render``: Generates the graphviz objects and renders the images
  - ``tex``: Generates the graphviz objects and prints the latex code
  - ``gif``: Generates the graphviz objects and creates a gif


Consider the file `example2.lp <https://github.com/potassco/clingraph/blob/master/examples/doc/example2/example2.lp>`_

.. include:: ../../examples/doc/example2/example2.lp
  :literal:

- **Facts output** ``out=facts``

The output is a string containing the facts for all graphs provided that are part of the syntax, after preprocessing

.. code:: shell

  $ clingraph example2.lp --out=facts

.. code:: shell

  node(tom,toms_family).
  node(max,toms_family).
  node(bill,bills_family).
  node(jen,bills_family).
  graph(toms_family).
  graph(bills_family).
  edge((tom,max),toms_family).
  edge((bill,jen),bills_family).

- **Dot output** ``out=dot``

The output is a string containing the graph in `DOT language <https://en.wikipedia.org/wiki/DOT_(graph_description_language)>`_

.. code:: shell

  $ clingraph example2.lp --out=dot

.. code:: shell

  graph toms_family {
    tom
    max
    tom -- max
  }

  graph bills_family {
    bill
    jen
    bill -- jen
  }

Output can also be saved in an individual files per graph with argument ``--save``.
The file is saved in directory ``--dir`` and using the name formatting ``--name-format``.

.. code:: shell

  $ clingraph example2.lp --out=dot --save --dir='out' --name-format='new_version_{graph_name}'

.. code:: shell

  File saved in out/new_version_toms_family.dot
  File saved in out/new_version_bills_family.dot


- **Render output** ``out=render``

The graphs will be rendered and saved in files with a given format and engine

.. code:: shell

  $ clingraph example2.lp --out=render --format=png

.. code:: shell

  Image saved in out/toms_family.png
  Image saved in out/bills_family.png

.. list-table:: 

    * - .. figure:: ../../examples/doc/example2/toms_family.png

          ``out/toms_family.png``

      - .. figure:: ../../examples/doc/example2/bills_family.png

          ``out/bills_family.png``

- **Gif output** ``out=gif``

Generates a gif with the graph rendering. The order of the images can be provided with argument ``--sort`` based on the name.

  - ``asc-str``: Sort ascendent based on the graph name as a string
  - ``asc-int``: Sort ascendent based on the graph name as an integer
  - ``desc-str``: Sort descendent based on the graph name as a string
  - ``desc-int``: Sort descendent based on the graph name as an integer
  - ``name1,...,namex``: A string with the order of the graph names separated by `,`

Additionally the number of frames per second can be set with ``--fps``.
.. code:: shell

  $ clingraph example2.lp --out=gif --sort=desc --name-format=families_gif

.. code:: shell

  Image saved in out/images/gif_image_toms_family_0.png
  Image saved in out/images/gif_image_bills_family_0.png
  Gif saved in out/families_gif.gif

- **Latex output** ``out=tex``

See the :ref:`latex integration section<latex integration>`.


Partial output
++++++++++++++

Graphs can be selected by name to work only with a subset of the output

.. code:: shell

  $ clingraph example2.lp --out=dot --select-graph=toms_family

.. code:: shell

  graph toms_family {
    tom
    max
    tom -- max
  }


Clingo integration
==================

These features allow the usage of logic programs with rules to define the visualization. 
This is done in integration with clingo, letting the user handle multiple stable models.


.. note:: 
  **Good practices**

  We advice the user to keep the visualization encoding separate from the encodings used to solve the problem.
  This visualization encoding can include rules but no choices, those should be handled in the encoding.

Consider the encoding `example5_encoding.lp <https://github.com/potassco/clingraph/blob/master/examples/doc/example5/example5_encoding.lp>`_ 
that has two stable models.

.. include:: ../../examples/doc/example5/example5_encoding.lp
  :literal:

And a different file `example5_viz.lp <https://github.com/potassco/clingraph/blob/master/examples/doc/example5/example5_viz.lp>`_ 
for the visualization encoding.

.. include:: ../../examples/doc/example5/example5_viz.lp
  :literal:

Piping json output
++++++++++++++++++

.. warning:: 
  This integration is only supports special characters in strings, such as scaped quotes ``attr(node,a,label,"Quotes\"")``, when using ``clingo >= 5.5.2``.


- Run clingo to obtain the two stable models formatted as json with option ``--outf=2```

.. code:: shell

  $ clingo example5_encoding.lp example5_viz.lp -n0 --outf=2


.. code:: shell
    
  {
    "Solver": "clingo version 5.5.1",
    "Input": [
      "examples/doc/example5/example5_encoding.lp","examples/doc/example5/example5_viz.lp"
    ],
    "Call": [
      {
        "Witnesses": [
          {
            "Value": [
              "node(a)", "person(a)", "attr(node,a,color,blue)"
            ]
          },
          {
            "Value": [
              "node(b)", "person(b)", "attr(node,b,color,red)"
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


- Pipe clingos json output to clingraph

.. code:: shell

  $ clingo example5_encoding.lp example5_viz.lp -n0 --outf=2 | clingraph --out=dot


.. code:: shell
    
  WARNING:  - Outputing multiple models in stdout.
  graph default {
    a [color=blue]
  }

  graph default {
    b [color=red]
  }

- Load a json file 

.. code:: shell

  $ clingo example5_encoding.lp example5_viz.lp -n0 --outf=2 > out/example5.json ; clingraph out/example5.json --out=dot


.. code:: shell
    
  WARNING:  - Outputing multiple models in stdout.
  graph default {
    a [color=blue]
  }

  graph default {
    b [color=red]
  }

- Select a single model using the model number starting with index 0

.. code:: shell

  $ clingo example5_encoding.lp example5_viz.lp -n0 --outf=2 | clingraph --out=dot --select-model=1


.. code:: shell
    
  graph default {
    b [color=red]
  }


Define the visualization encoding
+++++++++++++++++++++++++++++++++

The visualization encoding can also be provided as a separate argument ``--viz-encoding``. 
This allows for integration projects using more complex scripts or applications. 
When passing a json as input, the visualization facts will be obtained by running clingo with the visualization encoding for each stable model.

.. warning:: 
  The visualization encoding should not include any choices, only the first stable model will be considered.


.. code:: shell

  $ clingo example5_encoding.lp -n0 --outf=2 | clingraph --viz-encoding example5_viz.lp --out=render --format=png


.. code:: shell
    
  Image saved in out/0/default.png
  Image saved in out/1/default.png

.. list-table:: 

    * - .. figure:: ../../examples/doc/example5/default_1.png

          ``out/0/default.png``

      - .. figure:: ../../examples/doc/example5/default_0.png

          ``out/1/default.png``

.. _Latex:

Latex integration
=================

The integration will latex generates latex code for the graphs using the `dot2tex <https://dot2tex.readthedocs.io/en/latest>`_ package. This feature allows the user to include mathematical notation in the labels.

.. warning:: To use math notation (``$``) in labels, we advise the user to use the ``texlbl`` special attribute for the latex label instead of the normal ``label`` attribute. This will avoid problems with the escape characters. Note that edges require a ``label`` attribute to be defined (even if it is empty) in order for the ``texlbl`` attribute to have an effect. Additionally, the backslash ``\`` must be escaped.


Consider the file `example6.lp <https://github.com/potassco/clingraph/blob/master/examples/doc/example6/example6.lp>`_

.. include:: ../../examples/doc/example6/example6.lp
  :literal:


Run cligraph to obtain the latex file using the output option ``--out=tex``. 
The optional parameters in ``--tex-param`` are passed to `dot2tex <https://dot2tex.readthedocs.io/en/latest/usage_guide.html>`_.
This parameter should be a string ``arg_name=arg_value``.

.. code:: shell

  $ clingraph example6.lp --out=tex --tex-param="crop=True" --save

Then, the compilation can be done using a package like ``pdflatex``

.. code:: shell

  File saved in out/default.tex

.. code:: shell

  $ pdflatex out/default.tex ; open default.pdf


We can see compare the two outputs using ``--out=tex`` and ``--out=render``:

.. list-table:: 

    * - .. figure:: ../../examples/doc/example6/default.png

           *Graph rendered by graphviz* ``--out=render``

      - .. figure:: ../../examples/doc/example6/latex.png

           *Graph compiled by latex* ``--out=tex``


