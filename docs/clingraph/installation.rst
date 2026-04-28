Installation
############

Clingraph requires Python 3.9 or greater


Installing with pip
===================

The python clingraph package can be found `here <https://pypi.org/project/clingraph/>`_.

.. warning::
    For the installation using ``pip`` the user must first install `graphviz <https://www.graphviz.org/download/>`_  (version 2.50 or greater) manually.

.. code-block:: console

    $ pip install clingraph

The following dependencies used in `clingraph` are optional.

#. `tex`: For latex code generation.
#. `gif`: For gifs generation.

To include them in the installation use:

.. code-block:: console

    $ pip install clingraph[tex,gif]



Installing from source
======================

The project is hosted on github at https://github.com/potassco/clingraph and can
also be installed from source. We recommend this only for development purposes.


.. code-block:: console

    $ git clone https://github.com/potassco/clingraph
    $ cd clingraph
    $ pip install .[dev,tex,gif]

.. warning::
    This makes clingraph available in the command line using ``python -m clingraph`` instead of ``clingraph``.
