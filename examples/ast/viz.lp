node(I) :- ast_node(I, _, _).

attr(graph_nodes, default, fontsize, 10).
attr(graph_nodes, default, shape, plain).
attr(node, I, (label, sep), "") :- ast_node(I, _, _).
attr(node, I, (label,   0), "<<table border='0' cellborder='1' cellspacing='0' cellpadding='3'><tr><td>") :- ast_node(I, _, _).
attr(node, I, (label,   1), I) :- ast_node(I, _, _).
attr(node, I, (label,   2), "</td><td>") :- ast_node(I, _, _).
attr(node, I, (label,   3), T) :- ast_node(I, type, T).
attr(node, I, (label,   4), "</td><td>") :- ast_node(I, variant, _).
attr(node, I, (label,   5), V) :- ast_node(I, variant, V).
attr(node, I, (label,   6), "</td></tr><tr><td colspan='2'>") :- ast_node(I, value, _), not ast_node(I, variant, _).
attr(node, I, (label,   6), "</td></tr><tr><td colspan='3'>") :- ast_node(I, value, _), ast_node(I, variant, _).
attr(node, I, (label,   7), "<font face='monospace'>") :- ast_node(I, value, _).
attr(node, I, (label,   8), V) :- ast_node(I, value, V).
attr(node, I, (label,   9), "</font>") :- ast_node(I, value, _).
attr(node, I, (label, 127), "</td></tr></table>>") :- ast_node(I, _, _).

edge(I) :- ast_edge(I, _, _).

attr(graph_edges, default, fontsize, 10).
attr(edge, I, label, L) :- ast_edge(I, key, L).