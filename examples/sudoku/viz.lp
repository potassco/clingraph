#const dim = 3.

%%%%%%%%%%%%%%%%%%%%%%%% Visualization
graph(sudoku).

% Nodes
node(pos(X,Y), sudoku):- pos(X,Y).
attr(node, pos(X,Y), label, V):- sudoku(X,Y,V).
attr(node, pos(X,Y), shape, square):- sudoku(X,Y,V).
attr(node, pos(X,Y), style, filled):- sudoku(X,Y,V).
attr(node, pos(X,Y), fontsize, 30):- sudoku(X,Y,V).
attr(node, pos(X,Y), width, "1"):- sudoku(X,Y,V).
attr(node, pos(X,Y), pos, @pos(X,Y)):- pos(X,Y).
attr(node, pos(X,Y), fillcolor, lightblue):- pos(X,Y), (((X-1)/dim)+((Y-1)/dim))\2==0.
attr(node, pos(X,Y), fontcolor, gray50):- sudoku(X,Y,V), not initial(X,Y,_).
