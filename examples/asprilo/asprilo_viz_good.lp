#script (python)
from clingo.symbol import String
def pos(x,y):
    return String(f"{str(x)},{str(y)}!")

def join(base,*args):
    return String(str(base).strip('"').join([str(x).strip('"') for x in args]))
#end.

% One graph per time
viz_graph(T):-time(T).
viz_attr(graph, G, label, ""):- viz_graph(G).
viz_attr(graph, G, style, invis):- viz_graph(G).
viz_attr(graph, G, type, digraph):- viz_graph(G).
viz_attr(graph, G, nodesep, 1):- viz_graph(G).
viz_attr(graph, G, newrank, true):- viz_graph(G).


% Global node/edge attributes
viz_attr(class, node, width, "0.5").
viz_attr(class, node, height, "0.5").
viz_attr(class, node, fixedsize, "shape").
viz_attr(class, node, fontsize, "8").
viz_attr(class, node, style, "filled").
viz_attr(class, edge, shape, vee).
viz_attr(class, edge, style, dotted).
viz_attr(class, edge, arrowsize, "0.5").


% One node per position
viz_node((X,Y,T),T) :- position((X,Y)), time(T).
viz_attr(node,(X,Y,T),pos,@pos(X,Y)) :- position((X,Y)),time(T).

% --------------  picking station
viz_attr(node,(X,Y,T),shape,"doublecircle"):-
    position(station(S),(X,Y)),
    time(T).
viz_attr(node,(X,Y,T),style,"wedged"):-
    position(station(S),(X,Y)),
    time(T),
    position(_,(X,Y),T).

viz_attr(node,(X,Y,T),style,"filled"):-
    position(station(S),(X,Y)),
    time(T),
    not position(_,(X,Y),T).
viz_attr(node,(X,Y,T),label,""):-
    position(station(S),(X,Y)),
    time(T),
    not position(_,(X,Y),T).
viz_attr(node,(X,Y,T),fillcolor,"gold"):-
    position(station(S),(X,Y)),
    time(T),
    not position(_,(X,Y),T).

% --------------  robot
viz_attr(node,(X,Y,T),shape,circle):-
    position(robot(R),(X,Y),T), 
    not position(shelf(_),(X,Y),T).
viz_attr(node,(X,Y,T),label,@join("","R",R)):-
    position(robot(R),(X,Y),T),
    not position(shelf(_),(X,Y),T).
viz_attr(node,(X,Y,T),fillcolor,@join("","/pubu9/",1+R)):-
    position(robot(R),(X,Y),T),
    not position(station(_),(X,Y)),
    not position(shelf(_),(X,Y),T).

% --------------  shelf
viz_attr(node,(X,Y,T),shape,"box"):-
    position(shelf(S),(X,Y),T),
    not position(robot(_),(X,Y),T).
viz_attr(node,(X,Y,T),label,@join("","S",S)):-
    position(shelf(S),(X,Y),T),
    not position(robot(_),(X,Y),T).
viz_attr(node,(X,Y,T),fillcolor,@join("","/orrd9/",1+S)):-
    position(shelf(S),(X,Y),T),
    not position(station(_),(X,Y)),
    not position(robot(_),(X,Y),T).



% --------------  robot on same position
viz_attr(node,(X,Y,T),fillcolor,@join("","/pubu9/",1+R,":","/orrd9/",1+S)):-
    position(shelf(S),(X,Y),T), 
    position(robot(R),(X,Y),T),
    not position(station(_),(X,Y)).
viz_attr(node,(X,Y,T),fillcolor,@join("","/pubu9/",1+R,":","/orrd9/",1+S,":","gold")):-
    position(shelf(S),(X,Y),T), 
    position(robot(R),(X,Y),T),
    position(station(_),(X,Y)).
viz_attr(node,(X,Y,T),fillcolor,@join("","/orrd9/",1+S,":","gold")):-
    position(shelf(S),(X,Y),T), 
    not position(robot(_),(X,Y),T),
    position(station(_),(X,Y)).
viz_attr(node,(X,Y,T),fillcolor,@join("","/pubu9/",1+R,":","gold")):-
    not position(shelf(_),(X,Y),T), 
    position(robot(R),(X,Y),T),
    position(station(_),(X,Y)).

viz_attr(node,(X,Y,T),penwidth,3):-
    position(shelf(S),(X,Y),T), 
    position(robot(R),(X,Y),T),
    carries(robot(R),shelf(S),T).

viz_attr(node,(X,Y,T),shape,"square"):-
    position(shelf(S),(X,Y),T),
    position(robot(R),(X,Y),T).
viz_attr(node,(X,Y,T),style,"striped"):-
    position(shelf(S),(X,Y),T),
    position(robot(R),(X,Y),T).

viz_attr(node,(X,Y,T),label,@join("","R",R," ","S",S)):-
    position(shelf(S),(X,Y),T),
    position(robot(R),(X,Y),T).

% --------------  empty position
viz_attr(node,(X,Y,T),shape,point):- 
    position((X,Y)), not position(_,(X,Y),T),
    not position(station(_),(X,Y)),time(T).
viz_attr(node,(X,Y,T),penwidth,30):- 
    position((X,Y)), not position(_,(X,Y),T),
    not position(station(_),(X,Y)),time(T).
viz_attr(node,(X,Y,T),color,white):- 
    position((X,Y)), not position(_,(X,Y),T),
    not position(station(_),(X,Y)),time(T).
viz_attr(node,(X,Y,T),fillcolor,gray):- 
    position((X,Y)), not position(_,(X,Y),T),
    highway((X,Y)),
    not position(station(_),(X,Y)),time(T).
viz_attr(node,(X,Y,T),fillcolor,black):- 
    position((X,Y)), not position(_,(X,Y),T),
    not highway((X,Y)),
    not position(station(_),(X,Y)),time(T).
viz_attr(node,(X,Y,T),label,""):-
    position((X,Y)), not position(_,(X,Y),T),
    not position(station(_),(X,Y)),time(T).


viz_attr(node,(X,Y,T),fontcolor,"gray"):-
    position((X,Y)), not position(_,(X,Y),T),time(T),not position(station(_),(X,Y)).


viz_edge(((X,Y,T),(X+DX,Y+DY,T)),T):-
    move(robot(R),(DX,DY),T),
    position(robot(R),(X,Y),T-1).

