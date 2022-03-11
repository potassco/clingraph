### Sudoku

**Features used:**
- Multi model
- Multi model rendering
- Predicate prefix
- Engine
- Default graph
- HTML labels


`clingo examples/sudoku/encoding.lp examples/sudoku/instance.lp  -n 0 --outf=2 | clingraph  --view --dir='out/sudoku' --format=png --out=render --prefix=viz_ --engine=neato --default-graph=sudoku --viz-encoding=examples/sudoku/viz.lp --name-format=model_{model_number}`

#### First stable model
![](model_0.png)

#### Second stable model

![](model_1.png)
