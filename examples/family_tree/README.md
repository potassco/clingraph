### Family Tree (WIP)

A Family tree that expands using svg


**Features used:**
- SVG interaction

```
clingo examples/family_tree/encoding.lp --outf=2 --opt-mode=opt | clingraph --viz=examples/family_tree/viz.lp --type=digraph --view --format=svg --select-model=0 --out=render
```

Notice that you must download the `svg` [file](./default.svg) and run it on your computer. Otherwise GitHub will prevent the `svg` scripts from running.

![](default.png)
