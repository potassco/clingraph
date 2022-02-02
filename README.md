# clingraph

A visualizer for graphs defined as a set of facts computed from logic programs. Graphs are generated using [graphviz](https://graphviz.org) defined via fixed predicates from a list of facts. 


Clingraph also contains special features for integration with [clingo](https://potassco.org/clingo/) generation of gifs and latex code!

Try the package online: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/potassco/clingraph/development?labpath=docs%2Fnotebook.ipynb)
 


## Installation

### Requirements

- Python (version 3.8, 3.9, or 3.10)

##### Install with conda
We advise the user to install the dependencies using the provided conda environment:

```
conda env create -f environment.yml
conda activate clingraph
```

##### Manually install graphviz
Otherwise the user must manually install the dependencies:

This package requires the installation of 
- [pygraphviz](https://pygraphviz.github.io/documentation/stable/install.html)
  - [graphviz](https://www.graphviz.org) installed via [python-graphviz](https://anaconda.org/conda-forge/python-graphviz)

### Package

Standing on the root folder install the project and python dependencies:

```
pip install .
```

This will make the command `clingraph` available for usage as well as the python package with `import clingraph`.

## Run tests

```
pytest -v
```

## Usage

For the documentation of how to use the tool see our [documentation page](https://clingraph.readthedocs.io/en/latest/).

