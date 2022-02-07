Installation
############

Clingraph requires Python 3.8 or grater

Installing with conda (Beta version)
====================================

.. code-block:: bash

    $ conda install -c potassco/label/dev clingraph

.. note::
    The conda installation does not include optional dependencies for latex and gifs.
    The additional dependencies can also be installed with conda using: 

    .. code-block:: bash

        $ conda install -c conda-forge dot2tex imageio



Installing with pip (Beta version)
==================================

For the installation using ``pip`` the user must first install `graphviz <https://www.graphviz.org/download/>`_  manually.

.. code-block:: bash

    $ pip install --extra-index-url https://test.pypi.org/simple/ clingraph

The following dependencies used in `clingraph` are optional. 

#. `tex`: For latex code generation.
#. `gif`: For gifs generation.

To include them in the installation use:

.. code-block:: bash

    $ pip install --extra-index-url https://test.pypi.org/simple/ clingraph[tex,gif]


Installing with apt
===================

.. code-block:: bash

    $ sudo add-apt-repository ppa:potassco/wip

or 

.. code-block:: bash

    $ sudo apt install python3-clingraph


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

.. warning:: 
    This makes clingraph available in the command like using ``python -m clingraph`` instead of ``clingraph``.