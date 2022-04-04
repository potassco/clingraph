### Asprilo

Intra logistics robotics

**Features used:**
- Clingo integration
- Multi model
- Model selection
- Engine
- Gif

`clingo examples/asprilo/asprilo/asprilo.lp examples/asprilo/asprilo/instance2.lp -c horizon=20 --outf=2| clingraph --viz-encoding=examples/asprilo/asprilo_viz.lp  --out=animate --sort=asc-int  --engine=neato --dir='out/asprilo' --select-model=0 --type=digraph`

![](movie.gif)