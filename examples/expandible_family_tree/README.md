### Family Tree (WIP)

Idea of a Family tree that expands using svg

```
clingo examples/expandible_family_tree/encoding.lp --outf=2 --opt-mode=opt | clingraph --viz=examples/expandible_family_tree/viz.lp --type=digraph --view --format=svg --select-model=0 --out=render
```

Notice that you must download the `svg` file. Otherwise GitHub will prevent the `svg` scripts from running.
![](default.gif)
