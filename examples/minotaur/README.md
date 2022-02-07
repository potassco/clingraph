### Minotaur problem

The problem is described here:
* https://mybinder.org/v2/gh/potassco-asp-course/notebooks/HEAD?labpath=projects%2Fminotaur%2Fminotaur.ipynb

The image paths must be absolute, therefore the user must change the visualization encoding with the absolute path to the location of the image.

**Features used:**
- Multi model
- Multi graph
- Image attributes
- Model selection 
- Gif generation
- Gif special parameter
- Quiet mode


`clingo examples/minotaur/minotaur.lp --outf=2 | clingraph --prefix='viz_' --engine=neato --gif --format=png --dir='out/minotaur' --type=graph --json --select-model=1 --gif-param="fps=1" -q`
