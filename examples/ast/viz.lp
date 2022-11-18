hide(edge, I) :- ast_edge(I, _, _), I = (_, I2), ast_node(I2, type, "Location").
hide(node, I) :- hide(edge, (_, I)).
hide(edge, I) :- ast_edge(I, _, _), I = (I1, _), hide(node, I1).

node(I) :- ast_node(I, _, _), not hide(node, I).
edge(I) :- ast_edge(I, _, _), not hide(edge, I).

attr(graph_nodes, default, fontsize, 10).
attr(graph_nodes, default, shape, plain).
attr(node, I, (label, sep), "") :- node(I).
attr(node, I, (label,   0), "<<table border='0' cellborder='1' cellspacing='0' cellpadding='3'><tr><td>") :- node(I).
attr(node, I, (label,   1), I) :- node(I).
attr(node, I, (label,   2), "</td><td>") :- node(I).
attr(node, I, (label,   3), T) :- node(I), ast_node(I, type, T).
attr(node, I, (label,   4), "</td><td>") :- node(I), ast_node(I, variant, _).
attr(node, I, (label,   5), V) :- node(I), ast_node(I, variant, V).
attr(node, I, (label,   6), "</td></tr><tr><td colspan='2'>") :- node(I), ast_node(I, value, _), not ast_node(I, variant, _).
attr(node, I, (label,   6), "</td></tr><tr><td colspan='3'>") :- node(I), ast_node(I, value, _), ast_node(I, variant, _).
attr(node, I, (label,   7), "<font face='monospace'>") :- node(I), ast_node(I, value, _).
attr(node, I, (label,   8), V) :- node(I), ast_node(I, value, V).
attr(node, I, (label,   9), "</font>") :- node(I), ast_node(I, value, _).
attr(node, I, (label, 127), "</td></tr></table>>") :- node(I).

attr(graph_edges, default, fontsize, 10).
attr(edge, I, label, L) :- edge(I), ast_edge(I, key, L).
