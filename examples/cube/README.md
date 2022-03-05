### Cube

**Features used:**
- Piped from clingo as list of facts
- Simple dot output that can be piped to another thing

`clingo examples/cube/cube.lp  --out-atomf=%s. --warn=none | head -n5 | tail -n1| clingraph --out=dot`
