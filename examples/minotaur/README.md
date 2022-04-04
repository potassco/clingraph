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


`clingo examples/minotaur/minotaur.lp --outf=2 | clingraph --prefix='viz_' --engine=neato --out=animate --dir='out/minotaur' --type=graph --select-model=0 --fps=1 --name-format=minotaur`

![](minotaur.gif)
