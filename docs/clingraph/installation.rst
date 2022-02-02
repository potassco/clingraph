Installation
############

Clingraph requires Python 3.8 or grater

Installing with conda
=====================

.. code-block:: bash

    $ conda install clingraph

Installing with pip
=====================

For the installation using ```pip`` the user must first install `graphviz <https://www.graphviz.org/download/>`_  manually.

.. code-block:: bash

    $ pip install -u clingraph

The following dependencies used in `clingraph` are optional. 
- `tex`: For latex code generation.
- `gif`: For gifs generation.
- `ipython`: To show graphs in a jupyter notebook.

To include them in the installation use:

.. code-block:: bash

    $ pip install -u clingraph[tex,gif,ipython]


Installing from source
======================

The project is hosted on github at https://github.com/potassco/clingraph and can
also be installed from source. We recommend this only for development purposes.

With conda: 

.. code-block:: bash

    $ git clone https://github.com/potassco/clingraph
    $ cd clingraph
    $ conda env create -f environment.yml
    $ conda activate clingraph
    $ conda install pylint pytest -c conda-forge

With pip:

.. code-block:: bash

    $ git clone https://github.com/potassco/clingraph
    $ cd clingraph
    $ pip install .[dev,tex,gif,ipython]

.. warn:: 
    This makes clingraph available in the command like using ``python -m clingraph`` instead of ``clingraph``.