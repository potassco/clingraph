### Multi edge


Multi edges can be defined using a tuple of size 3 for the edge instead of size 2

`edge((N1,N2,Name))`

Where the connection is between node `N1` and node `N2` and the edge is called `Name`. 

**Features used:**
- Multi edges


`clingraph examples/multi_edge/encoding.lp --viz-encoding examples/multi_edge/viz.lp --out=render --view --type digraph`

![](default.png)
