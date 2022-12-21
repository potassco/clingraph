ast_show(node, 875).
ast_hide(edge, I) :- ast_edge(I, _, _), I = (_, I2), ast_node(I2, type, "Location").

ast_show(edge, I) :- ast_edge(I, _, _), I = (I1, _), ast_show(node, I1).
ast_show(node, I) :- ast_show(edge, (_, I)).

ast_hide(node, I) :- ast_hide(edge, (_, I)).
ast_hide(edge, I) :- ast_edge(I, _, _), I = (I1, _), ast_hide(node, I1).

node(I) :- ast_node(I, _, _), ast_show(node, I), not ast_hide(node, I).
edge(I) :- ast_edge(I, _, _), ast_show(edge, I), not ast_hide(edge, I).

attr(node, I, label, @concat(
    "<<table border='0' cellborder='1' cellspacing='0' cellpadding='3'>",
    "<tr>",
        "<td>{{id}}</td>",
        "<td>{{type}}</td>",
        "{% if variant %}<td>{{variant}}</td>{% endif %}",
    "</tr>",
    "{% if value %}",
        "<tr><td colspan='{{colspan}}'>",
            "<font face='monospace'> {{value}} </font>",
        "</td></tr>",
    "{% endif %}",
    "</table>>"
)) :- node(I).

attr(node, I, (label, id), I)
    :- node(I).
attr(node, I, (label, type), T)
    :- node(I), ast_node(I, type, T).
attr(node, I, (label, variant), V)
    :- node(I), ast_node(I, variant, V).
attr(node, I, (label, colspan), 2)
    :- node(I), ast_node(I, value, _), not ast_node(I, variant, _).
attr(node, I, (label, colspan), 3)
    :- node(I), ast_node(I, value, _), ast_node(I, variant, _).
attr(node, I, (label, value), @html_escape(V))
    :- node(I), ast_node(I, value, V).

attr(edge, I, label, L) :- edge(I), ast_edge(I, key, L).

attr(graph_nodes, default, fontsize, 10).
attr(graph_nodes, default, shape, plain).

attr(graph_edges, default, fontsize, 10).
