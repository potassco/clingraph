### Transition system

**Features used:**
- Latex integration
- Clingo integration
- Multi model rendering
- Default graph


`clingo examples/transition_system/light_system.lp examples/transition_system/viz.lp --outf=2 | clingraph --json  --type=digraph --select-model=1 --tex --default-graph=system --render`

This command can be followed by:

`pdflatex out/system.tex`

To compile the latex file into a pdf.