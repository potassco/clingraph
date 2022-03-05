### Asprilo

Intra logistics robotics

**Features used:**
- Clingo integration
- Multi model
- Model selection
- Predicate Prefix
- Engine
- Gif

`clingo examples/asprilo/asprilo/asprilo.lp examples/asprilo/asprilo/instance2.lp -c horizon=20 --outf=2| clingraph --json  --viz-encoding=examples/asprilo/asprilo_viz.lp  --out=gif --sort=asc-int  --prefix='viz_' --engine=neato --dir='out/asprilo' --select-model=0`

![](movie.gif)