% %%%%%%%%%%%%%%%%%%%%%%%%% Encoding

#const dim = 3.

val(1..dim*dim).
pos(X,Y) :- val(X), val(Y).

subgrid(X,Y,(((X-1)/dim)*dim+((Y-1)/dim))) :- pos(X,Y).

1 { sudoku(X,Y,V) : val(V) } 1 :- pos(X,Y).

:- sudoku(X,Y,V), sudoku(X',Y,V), X != X'.
:- sudoku(X,Y,V), sudoku(X,Y',V), Y != Y'.
:- sudoku(X,Y,V), sudoku(X',Y',V), subgrid(X,Y,S), subgrid(X',Y',S), (X,Y)!=(X',Y').


sudoku(X,Y,V) :- initial(X,Y,V).
