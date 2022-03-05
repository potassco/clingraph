### Transition system

**Features used:**
- Latex integration
- Clingo integration
- Multi model rendering
- Default graph
- Load from file
- Viz encoding
- Save option


`clingraph examples/transition_system/light_system.lp --type=digraph --default-graph=system --out=tex --viz-encoding=examples/transition_system/viz.lp --save`

This command can be followed by:

`pdflatex out/system.tex`

To compile the latex file into a pdf.


![](system.png)
