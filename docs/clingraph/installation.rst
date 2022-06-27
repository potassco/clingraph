Installation
############

Clingraph requires Python 3.8 or greater

Installing with conda
=====================

The conda clingraph package can be found `here <https://anaconda.org/potassco/clingraph>`_.

.. code-block:: bash

    $ conda install -c potassco clingraph 
    $ conda install -c potassco/label/dev clingraph

.. note::
    The conda installation does not include optional dependencies for latex and gifs.
    The additional dependencies can also be installed with conda using: 

    .. code-block:: bash

        $ conda install -c conda-forge dot2tex imageio



Installing with pip 
===================

The python clingraph package can be found `here <https://pypi.org/project/clingraph/>`_.

.. warning:: 
    For the installation using ``pip`` the user must first install `graphviz <https://www.graphviz.org/download/>`_  (version 2.50 or greater) manually.

.. code-block:: bash

    $ pip install clingraph

The following dependencies used in `clingraph` are optional. 

#. `tex`: For latex code generation.
#. `gif`: For gifs generation.

To include them in the installation use:

.. code-block:: bash

    $ pip install clingraph[tex,gif]



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
    $ pip install .[dev,tex,gif]

.. warning:: 
    This makes clingraph available in the command line using ``python -m clingraph`` instead of ``clingraph``.
