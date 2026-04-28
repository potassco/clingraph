# Changes

## v1.2.0

```
Migrated repository to use noz and other CI
Conda installation is not supported anymore, see documentation for details on installation
```

## v1.1.2

```
Added functionality to the context to be called with @ for integration with clinguin system
@ clinguin_fontname: To get the fontname of clinguin
@ color : To get colors with an opacity. This are the same colors used in clinguin
Example for reified programs
Link to paper
Fixed small bugs
```

## v1.1.1

```
Updated imageio package do to deprecation on fps argument
```

## v1.1.0

```
This new realease includes new features for interactivity and formatting. There might arise issues on backwards compatibility with the previous use of tuples as attrubute names, see below for details.

See the documentation for details.

🎖New features
Improved efficiency
SVG integractuive output
Templates to format strings using Jinja
New examples for integractivity, templates and visualizing the program structure
⚠️ Backwards compatibility
In version 1.0.0 one could use tuples as names for attributes where the second value would be a number indicating the position.

Example from version 1.0.0

attr(node,a,label,"Other").
attr(node,a,(label,1),"Andreas").
attr(node,a,(label,2),"Mark").
attr(node,a,(label,sep),";").
With the new templating feature, the behaviour changes, these are the key differences.

Before: Labels without an index would be in the first position
Now: Labels without tuple format are considered templates

Before: The key "sep" was used to indicate the separator
Now: Separators can be defined in the template

Example addaped to new version 1.1.0

attr(node,a,label,"{name1};{name2};{name3}").
attr(node,a,(label,name1),"Other").
attr(node,a,(label,name2),"Andreas").
attr(node,a,(label,name3),"Mark").
```

## v1.0.0

🥇 The first release of clingraph, together with the expected publication in
LPNMR 22. All details can be found in the documentation.
