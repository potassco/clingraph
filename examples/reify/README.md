### Run example for reified format

For this example one must first compute the reification using `gringo` 

`echo "$(gringo examples/reify/program1.lp --output=reify)" "$(cat examples/reify/viz_basic.lp)" | clingraph --dir='out/reify' --default-graph=program --format=pdf`

Run example that uses theory atoms

`echo "$(gringo examples/reify/program2.lp --output=reify)" "$(cat examples/reify/viz_basic.lp) $(cat examples/reify/viz_theory.lp)" | clingraph --dir='out/reify' --default-graph=program --format=pdf --view`