% %%%%%%%%%%%%%%%%%%%%%%%%% Visualization

#script (python)
from clingo.symbol import String
def pos(x,y):
    return String(f"{str(x)},{str(y)}!")
#end.

graph(I):- _step_type(_,I).
attr(graph,I,(label,0),T):- _step_type(T,I).
attr(graph,I,(label,1),"level:"):- _step_type(T,I).
attr(graph,I,(label,2),L):- _step_type(T,I), _level(L).

% Global graph attributes
attr(graph, I, nodesep, 1):-graph(I).
attr(graph, I, newrank, true):-graph(I).

% Global node attributes
attr(graph_nodes, I, shape, square):-graph(I).
attr(graph_nodes, I, style, filled):-graph(I).
attr(graph_nodes, I, fillcolor, white):-graph(I).
attr(graph_nodes, I, width, "0.8"):-graph(I).

% Nodes
node(pos(X,Y), I):- _true(pos(X,Y)), graph(I).
attr(node, pos(X,Y), pos, @pos(X,Y)):- _true(pos(X,Y)).
attr(node, pos(X,Y), fillcolor, "gray"):- _true(sudoku(X,Y,V)), _true(initial(X,Y,_)).
attr(node, pos(X,Y), label, V):- _true(sudoku(X,Y,V)).
attr(node, pos(X,Y), label, V):- _undefined(sudoku(X,Y,V)).
attr(node, pos(X,Y), fontcolor, "gray"):- _undefined(sudoku(X,Y,V)).
attr(node, pos(X,Y), color, "green"):- _change(sudoku(X,Y,_)),_step_type(propagate,_).
attr(node, pos(X,Y), color, "red"):- _change(sudoku(X,Y,_)),_step_type(undo,_).


% Edges to show subgrids
edge((pos(X,Y),pos(X+1,Y)),I):- _true(pos(X,Y)), _true(pos(X+1,Y)), _true(subgrid(X,Y,S)), _true(subgrid(X+1,Y,S)), graph(I).
edge((pos(X,Y),pos(X,Y+1)),I):- _true(pos(X,Y)), _true(pos(X,Y+1)), _true(subgrid(X,Y,S)), _true(subgrid(X,Y+1,S)), graph(I).
