step(0..T) :- time(T).
position(station(S),P,T) :- position(station(S),P), step(T).

free(P,T) :- not position(_,P,T), position(P), step(T).

occo(P,T,robot(R)) :- position(robot(R),P,T),
               not position(station(_),P,T),
               not position(shelf(_),P,T).
occo(P,T,shelf(S)) :- position(shelf(S),P,T),
               not position(station(_),P,T).

% --- Graphs
graph(T) :- step(T).
attr(graph, G, nodesep, 1):- graph(G).
attr(graph_nodes, G, width, "0.5"):- graph(G).
attr(graph_nodes, G, fixedsize, "shape"):- graph(G).
attr(graph_nodes, G, style, "filled"):- graph(G).
attr(graph_nodes, G, fontsize, 10):- graph(G).

% --- Nodes
node((P,T),T) :- position(P), step(T).

% --- Edges (Movements)
edge((((X,Y),T),((X+DX,Y+DY),T)),T) :- move(robot(R),(DX,DY),T),
                                       position(robot(R),(X,Y),T-1).

% Position
attr(node,((X,Y),T),pos,@pos(X,YMax-Y)):- position((X,Y)), step(T), #max{Y':position((X',Y'))}=YMax.

% Label Simpler option without using HTML and without subindex
attr(node,(P,T),label,"R{{robot}}{%if shelf%}S{{shelf}}{%endif%}") :- position(robot(R),P,T).
attr(node,(P,T),(label,robot),R) :- position(robot(R),P,T).
attr(node,(P,T),(label,shelf),S) :- position(shelf(S),P,T).

% Shape
attr(node,(P,T),shape,"point") :- free(P,T).
attr(node,(P,T),shape,"doublecircle"):- position(station(S),P,T).
attr(node,(P,T),shape,"square") :- occo(P,T,shelf(_)).
attr(node,(P,T),shape,"circle") :- occo(P,T,robot(_)).

% Fillcolor
attr(node,(P,T),color,white) :- free(P,T).
attr(node,(P,T),fillcolor,gray) :- free(P,T), highway(P).
attr(node,(P,T),fillcolor,black) :- free(P,T), not highway(P).
attr(node,(P,T),fillcolor,"#99B88A") :- position(station(_),P,T).
attr(node,(P,T),colorscheme,"orrd9") :- occo(P,T,shelf(_)).
attr(node,(P,T),fillcolor,S) :- occo(P,T,shelf(S)).
attr(node,(P,T),colorscheme,"blues9") :- occo(P,T,robot(_)).
attr(node,(P,T),fillcolor,R) :- occo(P,T,robot(R)).

% Penwidth
attr(node,(P,T),penwidth,30) :- free(P,T).
attr(node,(P,T),penwidth,2) :- position(robot(R),P,T), carries(robot(R),shelf(S),T).
