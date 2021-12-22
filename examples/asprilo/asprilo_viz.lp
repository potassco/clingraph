#script (python)
from clingo.symbol import String
def pos(x,y):
    return String(f"{str(x)},{str(y)}!")

def join(base,*args):
    return String(str(base).strip('"').join([str(x).strip('"') for x in args]))
#end.

time0(0).
time0(T):-time(T).
% One graph per time
viz_graph(T):-time0(T).
viz_graph(0).
viz_attr(graph, G, label, ""):- viz_graph(G).
viz_attr(graph, G, style, invis):- viz_graph(G).
viz_attr(graph, G, type, digraph):- viz_graph(G).
viz_attr(graph, G, nodesep, 1):- viz_graph(G).
viz_attr(graph, G, newrank, true):- viz_graph(G).


% Global node/edge attributes
viz_attr(graph_nodes, G, width, "0.5"):- viz_graph(G).
viz_attr(graph_nodes, G, height, "0.5"):- viz_graph(G).
viz_attr(graph_nodes, G, fixedsize, "shape"):- viz_graph(G).
viz_attr(graph_nodes, G, fontsize, "8"):- viz_graph(G).
viz_attr(graph_nodes, G, style, "filled"):- viz_graph(G).
viz_attr(graph_edges, G, shape, vee):- viz_graph(G).
viz_attr(graph_edges, G, style, dotted):- viz_graph(G).
viz_attr(graph_edges, G, arrowsize, "0.5"):- viz_graph(G).


% Movements as edges
viz_edge(((X,Y,T),(X+DX,Y+DY,T)),T):-
    move(robot(R),(DX,DY),T),
    position(robot(R),(X,Y),T-1).

size(X,Y):- #max{X':position((X',Y'))}=X, #max{Y':position((X',Y'))}=Y.
% One node per position
viz_node((X,Y,T),T):-position((X,Y)),time0(T).
viz_attr(node, (X,Y,T),pos,@pos(X,YMax-Y)):- position((X,Y)), time0(T), size(XMax,YMax).

% Shape
viz_attr(node, (X,Y,T),shape,"doublecircle"):-
    viz_node((X,Y,T),T),
    position(station(S),(X,Y)).
viz_attr(node, (X,Y,T),shape,"circle"):-
    position(robot(R),(X,Y),T), 
    not position(shelf(_),(X,Y),T),
    not position(station(_),(X,Y)).
viz_attr(node, (X,Y,T),shape,"box"):-
    position(shelf(S),(X,Y),T),
    not position(robot(_),(X,Y),T),
    not position(station(_),(X,Y)).
viz_attr(node, (X,Y,T),shape,"square"):-
    position(shelf(S),(X,Y),T),
    position(robot(R),(X,Y),T),
    not position(station(_),(X,Y)).
viz_attr(node, (X,Y,T),shape,"point"):- 
    viz_node((X,Y,T),T),
    not position(_,(X,Y),T),
    not position(station(_),(X,Y)).

% Label
viz_attr(node, (X,Y,T),label,""):-
    viz_node((X,Y,T),T),
    not position(_,(X,Y),T).
viz_attr(node, (X,Y,T),label,@join("","R",R)):-
    position(robot(R),(X,Y),T),
    not position(shelf(_),(X,Y),T).
viz_attr(node, (X,Y,T),label,@join("","S",S)):-
    position(shelf(S),(X,Y),T),
    not position(robot(_),(X,Y),T).
viz_attr(node, (X,Y,T),label,@join("","R",R," ","S",S)):-
    position(shelf(S),(X,Y),T),
    position(robot(R),(X,Y),T).

% Fillcolor
viz_attr(node, (X,Y,T),fillcolor,"gold"):-
    viz_node((X,Y,T),T),
    position(station(S),(X,Y)),
    not position(_,(X,Y),T).
viz_attr(node, (X,Y,T),fillcolor,@join("","/pubu9/",1+R)):-
    position(robot(R),(X,Y),T),
    not position(station(_),(X,Y)),
    not position(shelf(_),(X,Y),T).
viz_attr(node, (X,Y,T),fillcolor,@join("","/orrd9/",1+S)):-
    position(shelf(S),(X,Y),T),
    not position(station(_),(X,Y)),
    not position(robot(_),(X,Y),T).
viz_attr(node, (X,Y,T),fillcolor,@join("","/pubu9/",1+R,":","/orrd9/",1+S)):-
    position(shelf(S),(X,Y),T), 
    position(robot(R),(X,Y),T),
    not position(station(_),(X,Y)).
viz_attr(node, (X,Y,T),fillcolor,@join("","/pubu9/",1+R,":","/orrd9/",1+S,":","gold")):-
    position(shelf(S),(X,Y),T), 
    position(robot(R),(X,Y),T),
    position(station(_),(X,Y)).
viz_attr(node, (X,Y,T),fillcolor,@join("","/orrd9/",1+S,":","gold")):-
    position(shelf(S),(X,Y),T), 
    not position(robot(_),(X,Y),T),
    position(station(_),(X,Y)).
viz_attr(node, (X,Y,T),fillcolor,@join("","/pubu9/",1+R,":","gold")):-
    not position(shelf(_),(X,Y),T), 
    position(robot(R),(X,Y),T),
    position(station(_),(X,Y)).
viz_attr(node, (X,Y,T),color,white):- 
    position((X,Y)), not position(_,(X,Y),T),
    not position(station(_),(X,Y)),time0(T).
viz_attr(node, (X,Y,T),fillcolor,gray):- 
    position((X,Y)), not position(_,(X,Y),T),
    highway((X,Y)),
    not position(station(_),(X,Y)),time0(T).
viz_attr(node, (X,Y,T),fillcolor,black):- 
    position((X,Y)), not position(_,(X,Y),T),
    not highway((X,Y)),
    not position(station(_),(X,Y)),time0(T).

% Penwidth
viz_attr(node, (X,Y,T),penwidth,30):- 
    position((X,Y)), not position(_,(X,Y),T),
    not position(station(_),(X,Y)),time0(T).
viz_attr(node, (X,Y,T),penwidth,2):-
    position(shelf(S),(X,Y),T), 
    position(robot(R),(X,Y),T),
    carries(robot(R),shelf(S),T).

% Style
viz_attr(node, (X,Y,T),style,"wedged"):-
    position(station(S),(X,Y)),
    time(T),
    position(_,(X,Y),T).
viz_attr(node, (X,Y,T),style,"filled"):-
    position(station(S),(X,Y)),
    time(T),
    not position(_,(X,Y),T).
viz_attr(node, (X,Y,T),style,"striped"):-
    position(shelf(S),(X,Y),T),
    position(robot(R),(X,Y),T).
