### Graph coloring

**Features used:**
- Clingo integration
- Multi model
- Rendering
- Model selection
- View

```console
clingo examples/color/color.lp  --outf=2 | clingraph --out=render  --view --dir='out/color' --format=png --select-model=0 -log=info
```

![](https://raw.githubusercontent.com/potassco/clingraph/master/examples/color/default.png)

- `color.lp`
```prolog
node(1..6).

edge(
    (1,2); (1,3); (1,4);
    (2,4); (2,5); (2,6);
    (3,4); (3,5);
    (5,6)
).

color(red; green; blue).

{ assign(N, C) : color(C) } = 1 :- node(N).

:- edge((N, M)), assign(N, C), assign(M, C).

#show node/1.
#show edge/1.
#show attr(node, N, style, filled): node(N).
#show attr(node, N, color, C) : assign(N, C).
```
