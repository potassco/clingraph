% Compute visualization with 
%   cat sudoku.lp| python graspviz.py | dot -Kfdp -n -Tpng -o sudoku.png


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


% %%%%%%%%%%%%%%%%%%%%%%%%% Visualization

#script (python)
from clingo.symbol import String
def pos(x,y):
    return String(f"{str(x)},{str(y)}!")
#end.

% Name of graph
viz_attr(graph, sudoku, name, "Sudoku").

% Global graph attributes
viz_attr(graph, sudoku, nodesep, 1).
viz_attr(graph, sudoku, newrank, true).

% Global node attributes
viz_attr(graph_nodes, sudoku, shape, square).
viz_attr(graph_nodes, sudoku, style, filled).
viz_attr(graph_nodes, sudoku, fillcolor, white).

% Nodes
viz_node(pos(X,Y)):- pos(X,Y).
viz_attr(node, pos(X,Y), label, V):- pos(X,Y), sudoku(X,Y,V).
viz_attr(node, pos(X,Y), fillcolor, gray):- initial(X,Y,_).
viz_attr(node, pos(X,Y), pos, @pos(X,Y)):- pos(X,Y).

% Edges to show subgrids
viz_edge((pos(X,Y),pos(X+1,Y))):- pos(X,Y), pos(X+1,Y), subgrid(X,Y,S), subgrid(X+1,Y,S).
viz_edge((pos(X,Y),pos(X,Y+1))):- pos(X,Y), pos(X,Y+1), subgrid(X,Y,S), subgrid(X,Y+1,S).



% %%%%%%%%%%%%%%%%%%%%%%%%% Instance

initial(5,1,8).
initial(6,2,7).
initial(7,1,4).
initial(8,2,2).
initial(8,1,6).
initial(9,2,9).
initial(3,3,9).
initial(4,3,3).
initial(6,3,6).
initial(7,3,5).
initial(8,3,7).
initial(1,4,7).
initial(2,4,6).
initial(4,4,4).
initial(7,4,9).
initial(8,4,3).
initial(2,5,3).
initial(3,5,2).
initial(4,5,8).
initial(7,5,7).
initial(9,5,5).
initial(1,6,9).
initial(2,6,1).
initial(3,6,8).
initial(8,6,4).
initial(9,6,6).
initial(1,7,6).
initial(5,7,7).
initial(6,7,8).
initial(8,7,9).
initial(9,7,4).
initial(2,8,7).
initial(3,8,3).
initial(4,8,6).
initial(5,8,9).
