### N-queens problem

See definition of the problem [here](https://en.wikipedia.org/wiki/Eight_queens_puzzle)

**Features used:**
- SVG interaction

`clingo examples/queens/encoding.lp --outf=2 | clingraph --viz-encoding=examples/queens/viz.lp --out=render  --engine=neato --format=svg`

Notice that you must download the `svg` [file](./default.svg) and run it on your computer. Otherwise GitHub will prevent the `svg` scripts from running.

![](queens-1.png)