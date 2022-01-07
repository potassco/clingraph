graph(house).
graph(bathroom, house).
graph(bedroom, house).

node(toilet,bathroom).
node(bed,bedroom).

edge((toilet,bed),house).


attr(graph, house, label, "Tom's House").
attr(graph, bathroom, style, dotted).
attr(graph, bathroom, label, "Bathroom").
attr(graph, bedroom, style, dotted).
attr(graph, bedroom, label, "Bedroom").

attr(graph_nodes, house, style, filled).
attr(graph_nodes, house, color, cyan).

attr(node, toilet, shape, circle).
attr(node, bed, shape, square).

attr(edge, (toilet,bed), color, red).
