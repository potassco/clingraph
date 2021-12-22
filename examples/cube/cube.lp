node(0..7).

edge((X, Y)) :-
    X1 = 0..1, X2 = 0..1, X4 = 0..1,
    Y1 = 0..1, Y2 = 0..1, Y4 = 0..1,
    |X1 - Y1| + |X2 - Y2| + |X4 - Y4| = 1,
    X = X1 + 2 * X2 + 4 * X4,
    Y = Y1 + 2 * Y2 + 4 * Y4,
    X < Y.

attr(edge,(X,Y), label, Y-X):- edge((X,Y)).

attr(edge, (X, Y), color, red  ) :- attr(edge, (X,Y), label, 1).
attr(edge, (X, Y), color, green) :- attr(edge, (X,Y), label, 2).
attr(edge, (X, Y), color, blue ) :- attr(edge, (X,Y), label, 4).


attr(edge, (X, Y), color, blue ) :- attr(edge, (X,Y), label, 4).
