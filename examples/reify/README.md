### Reified format

Shows the reification output of gringo 

**Features used:**
- Load from clingo
- Select graph
- View

For this example one must first compute the reification calling `gringo`.
Then we call clingo with our visualization encoding

`echo "$(gringo examples/reify/program1.lp --output=reify)" "$(cat examples/reify/viz_basic.lp)" | clingo --outf=2 | clingraph --dir='out/reify' --default-graph=program --format=pdf --json --select-model=1 --render --view`

Run example that uses theory atoms

`echo "$(gringo examples/reify/program2.lp --output=reify)" "$(cat examples/reify/viz_basic.lp) $(cat examples/reify/viz_theory.lp)" | clingo --outf=2 | clingraph --dir='out/reify' --default-graph=program --format=pdf --json --select-model=1 --render --view`