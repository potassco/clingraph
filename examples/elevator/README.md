### Elevator

A dynamic application of an elevator serving floors

**Features used:**
- Multi model
- Multi graph
- Model selection 
- Gif generation
- Gif special parameter

`clingo examples/elevator/encoding.lp examples/elevator/viz.lp examples/elevator/instance.lp --outf=2 | clingraph --json --out=gif --select-model=0 --dir='out/elevator' --fps=1 --sort=asc-int`

![](movie.gif)
