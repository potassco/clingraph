# clingraph

A **declarative visualizer for graphs** defined as a set of facts. The graphs are generated using [graphviz](https://graphviz.org) but are defined via fixed predicates that can be computed from logic programs. 

:sunglasses: Clingraph also contains **special features** for integration with **[clingo](https://potassco.org/clingo/)**, as well as for generating **latex** code and **gifs**!

Try clingraph **online** in a jupyter notebook :point_right: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/potassco/clingraph/master?labpath=notebook.ipynb)

 

:books: Look at the **documentation** in our [documentation page](https://clingraph.readthedocs.io/en/latest/).

Our **[examples folder](examples)** shows how to use the range of functionalities in different applications. 

- :turtle: Examples used in the [documentation](https://clingraph.readthedocs.io/en/latest/index.html) ([basic](examples/basic))
  - Attribute definition ([example1](examples/basic/example1))
  - Multi graphs ([example2](examples/basic/example2))
  - Subgraphs ([example3](examples/basic/example3))
  - Complex attributes ([example4](examples/basic/example4))
  - Clingo integration with multi model ([example5](examples/basic/example5))
  - Latex integration ([example6](examples/basic/example6))
- :turtle: Simple ([color](examples/color), [cube](examples/cube), [lights](examples/lights))
- :rabbit2: Advanced clingo integration ([sudoku](examples/sudoku), [reify](examples/reify), [transition_system](examples/transition_system))
  - Absolute positioning
  - Legends
  - Latex integration
- :rabbit2: Dynamic applications ([asprilo](examples/asprilo), [elevator](examples/elevator), [minotaur](examples/minotaur))
  - Clingo integration
  - Multi graphs
  - Gif generation



## Installation

### Requirements

- Python (version 3.8, 3.9, or 3.10)

For more installation options see our [documentation page](https://clingraph.readthedocs.io/en/latest/clingraph/installation.html).

##### Install from source 

###### With conda


```
  conda env create -f environment.yml
  conda activate clingraph
  conda install pylint pytest -c conda-forge
```

This makes clingraph available in the command like using `python -m clingraph` instead of `clingraph`.

###### With pip

- First manually install [graphviz](https://www.graphviz.org/download/)

- Then install the package with all the optional dependencies for development.

  ```
    pip install .[dev,tex,gif]
  ```

This will make the command `clingraph` available for usage as well as the python package with `import clingraph`.

## Run tests

```
pytest -v
```



