### Minotaur problem

The problem is described here:
* https://mybinder.org/v2/gh/potassco-asp-course/notebooks/HEAD?labpath=projects%2Fminotaur%2Fminotaur.ipynb

Run:
`clingo examples/minotaur/minotaur.lp --outf=2 | clingraph --prefix='viz_' --engine=neato --gif --format=png --dir='out/minotaur' --type=graph --json --select-model=1 --gif-param="fps=1" -q`
