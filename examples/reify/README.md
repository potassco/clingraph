### Run example for reified format

For this example one must first compute the reification using `gringo` 

`echo "$(gringo examples/reify/program1.lp --output=reify)" "$(cat examples/reify/viz.lp)" | clingraph --dir='out/reify' --default-graph=program --format=pdf`
