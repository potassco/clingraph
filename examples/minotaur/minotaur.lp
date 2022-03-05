%
% Instance
%

field(1..3,1..3).
start(2,1).
goal(3,2).
mino(2,3).
wall(2,1,2,2). wall(2,2,3,2). wall(2,2,2,3).
wall(X,Y,XX,YY) :- wall(XX,YY,X,Y).
maxsteps(10).


%
% Solution
% * Can be replaced by a general encoding that uses the output predicates at/3 and mino/3
%

at(2,1,0). at(1,1,1). at(2,1,2). at(3,1,3). at(3,2,4).
mino(2,3,0). mino(1,2,1). mino(2,2,2). mino(2,2,3). mino(2,2,4).


%
% Visualization
%

#script (python)
from clingo.symbol import String
def pos(x,y):
    return String(f"{str(x)},{str(y)}!")
#end.


% Graphs
viz_graph(T) :- at(_,_,T).

% Global graph attributes
viz_attr(graph, G, label, "") :- viz_graph(G).
viz_attr(graph, G, style, invis) :- viz_graph(G).
viz_attr(graph, G, nodesep, 1) :- viz_graph(G).
viz_attr(graph, G, newrank, true) :- viz_graph(G).

% Global node attributes
viz_attr(graph_nodes, G, shape, square) :- viz_graph(G).
viz_attr(graph_nodes, G, style, filled) :- viz_graph(G).
viz_attr(graph_nodes, G, fillcolor, white) :- viz_graph(G).
viz_attr(graph_nodes, G, label, "") :- viz_graph(G).
viz_attr(graph_nodes, G ,width,"0.5"):-viz_graph(G).
viz_attr(graph_nodes, G ,width,"0.5"):-viz_graph(G).

% Nodes
viz_node(field(X,Y,G),G):- field(X,Y), viz_graph(G).
viz_attr(node, field(X,Y,G), pos, @pos(X,Y)) :- field(X,Y), viz_graph(G).
viz_attr(node, field(X,Y,G), image,       "<absolute_path_to_clingraph>/examples/minotaur/mino.png") :- mino(X,Y,G),   viz_graph(G).

viz_attr(node, field(X,Y,G), image,      "<absolute_path_to_clingraph>/examples/minotaur/warrior.png") :- at(X,Y,G), viz_graph(G).
viz_attr(node, N, fixedsize,       "true") :- viz_attr(node,N,image,_).

viz_attr(node, field(X,Y,G), fillcolor,     green) :- at(X,Y,G), viz_graph(G),     goal(X,Y).
viz_attr(node, field(X,Y,G),     style,    dotted) :- goal(X,Y), viz_graph(G).

% Edges to show subgrids
viz_edge((field(X,Y,G),field(X+1,Y,G)),G):- field(X,Y), field(X+1,Y), not wall(X,Y,X+1,Y), viz_graph(G).
viz_edge((field(X,Y,G),field(X,Y+1,G)),G):- field(X,Y), field(X,Y+1), not wall(X,Y,X,Y+1), viz_graph(G).