node(john).
node(jane).
edge((john,jane)).

node(joe).
edge((john,joe,1)).
edge((john,joe,2)).

attr(graph, default, label, "Does family").

attr(graph_nodes, default, style, filled).
attr(node, john, label, "John Doe").
attr(node, jane, label, "Jane Doe").
