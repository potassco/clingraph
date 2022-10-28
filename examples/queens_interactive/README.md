### N-queens problem

See definition of the problem [here](https://en.wikipedia.org/wiki/Eight_queens_puzzle)

**Features used:**
- Clingo integration
- Neato
- Absolute Position


`clingo examples/queens/encoding.lp --outf=2 | clingraph --viz-encoding=examples/queens/viz.lp --out=render  --engine=neato`

Notice that you must download the `svg` file. Otherwise GitHub will prevent the `svg` scripts from running.

![](default.png)
