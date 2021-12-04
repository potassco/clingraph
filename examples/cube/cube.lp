node((0..1, 0..1, 0..1)).

edge(X, Y) :-
    node((X1, X2, X3)),
    node((Y1, Y2, Y3)),
    | X1 - Y1 | + | X2 - Y2 | + | X3 - Y3 | = 1,
    X = (X1, X2, X3),
    Y = (Y1, Y2, Y3),
    X < Y.
