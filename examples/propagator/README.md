### Propagator

Propagator to show clingos partial assignments while solving.
The case study for this problem is a Sudoku.

**Features used:**
- API usage
- Clingo integration
- Gif

For this example one must run just the propagator file using clingo.
The Graphs are created using clingraphs API inside the script.

`clingo examples/propagator/sudoku/encoding.lp examples/propagator/sudoku/instance.lp examples/propagator/clingraph-prop.lp`

![](movie.gif)

