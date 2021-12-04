clingraph_type(graph).

clingraph_node((0..1, 0..1, 0..1)).

clingraph_edge(X, Y) :-
    clingraph_node((X1, X2, X3)),
    clingraph_node((Y1, Y2, Y3)),
    | X1 - Y1 | + | X2 - Y2 | + | X3 - Y3 | = 1,
    X = (X1, X2, X3),
    Y = (Y1, Y2, Y3),
    X < Y.
