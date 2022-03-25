### Traveling sales problem

See definition of the problem [here](https://en.wikipedia.org/wiki/Travelling_salesman_problem)

**Features used:**
- Clingo integration
- Optimization
- Show statements


`clingo examples/traveling_sales_person/encoding.lp examples/traveling_sales_person/instance.lp --outf=2 --opt-mode=optN -q1 | clingraph --viz-encoding examples/traveling_sales_person/viz.lp --out=render --view`

![](default.png)
