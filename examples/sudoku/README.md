### Sudoku

**Features used:**
- Multi model
- Multi model rendering
- Predicate prefix
- Engine
- Default graph


`clingo examples/sudoku/sudoku.lp  -n 0 --outf=2 | clingraph  --view --dir='out/sudoku' --format=pdf --json --render --prefix=viz_ --engine=neato --default-graph=sudoku`
