#script (python)
from clingo.symbol import String
def pos(x,y):
    return String(f"{str(x)},{str(y)}!")
#end.
% --- Auxiliar
position(station(S),P,T):-position(station(S),P),step(T).
free(P,T):- position(P), not position(_,P,T),step(T).
step(0..T):-time(T).

% --- Graphs
graph(T):-step(T).
attr(graph, G, nodesep, 1):- graph(G).
attr(graph_nodes, G, width, "0.5"):- graph(G).
attr(graph_nodes, G, fixedsize, "shape"):- graph(G).
attr(graph_nodes, G, style, "filled"):- graph(G).
attr(graph_nodes, G, fontsize, 10):- graph(G).

% --- Edges (Movements)
edge((((X,Y),T),((X+DX,Y+DY),T)),T):- move(robot(R),(DX,DY),T), position(robot(R),(X,Y),T-1).

% --- Nodes
node((P,T),T):-position(P),step(T).

% Position
attr(node,((X,Y),T),pos,@pos(X,YMax-Y)):- position((X,Y)), step(T), #max{Y':position((X',Y'))}=YMax.

% Shape
attr(node,(P,T),shape,"doublecircle"):- position(station(S),P,T).
attr(node,(P,T),shape,"square"):- position(shelf(S),P,T), not position(station(_),P).
attr(node,(P,T),shape,"point"):- free(P,T).
attr(node,(P,T),shape,"plaintext"):- position(robot(R),P,T), not position(station(_),P), not position(shelf(_),P,T).
attr(node,(P,T),style,"solid"):- position(robot(R),P,T), not position(station(_),P), not position(shelf(_),P,T).

% Label Simpler option without using HTML and without subindex
attr(node,(P,T),(label,0),"R"):- position(robot(R),P,T).
attr(node,(P,T),(label,1),R):- position(robot(R),P,T).
attr(node,(P,T),(label,2),"S"):- position(shelf(S),P,T).
attr(node,(P,T),(label,3),S):- position(shelf(S),P,T).
attr(node,(P,T),(label,sep),""):- node((P,T),T).
% Label Using HTML for subindex
% attr(node,(P,T),(label,0),"< "):- node((P,T),T).
% attr(node,(P,T),(label,1),"R<sub>"):- position(robot(R),P,T).
% attr(node,(P,T),(label,2),R):- position(robot(R),P,T).
% attr(node,(P,T),(label,3),"</sub>"):- position(robot(R),P,T).
% attr(node,(P,T),(label,4),"S<sub>"):- position(shelf(S),P,T).
% attr(node,(P,T),(label,5),S):- position(shelf(S),P,T).
% attr(node,(P,T),(label,6),"</sub>"):- position(shelf(S),P,T).
% attr(node,(P,T),(label,7),">"):- node((P,T),T).
% attr(node,(P,T),(label,sep),""):- node((P,T),T).


% Fillcolor
attr(node,(P,T),fillcolor,"#99B88A"):- position(station(_),P,T).
attr(node,(P,T),colorscheme,"orrd9"):- position(shelf(S),P,T), not position(station(_),P,T).
attr(node,(P,T),fillcolor,S):- position(shelf(S),P,T), not position(station(_),P,T).
attr(node,(P,T),color,white):- free(P,T).
attr(node,(P,T),fillcolor,gray):- free(P,T), highway(P).
attr(node,(P,T),fillcolor,black):- free(P,T), not highway(P).

% Penwidth
attr(node,(P,T),penwidth,30):- free(P,T).
attr(node,(P,T),penwidth,2):- position(robot(R),P,T), carries(robot(R),shelf(S),T).