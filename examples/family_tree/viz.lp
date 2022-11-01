node(X):-person(X).
edge((X,Y)):-parent(X,Y).

attr(graph,default,label,"Modern Family Tree (click on the nodes to expand)"):-edge((X,Y)).
attr(node,X,style,"filled"):-node(X).

% linked(E,(X,Y)) X is linked to Y by edge E
linked((X,Y),(Y,X)):-edge((X,Y)).
linked((X,Y),(X,Y)):-edge((X,Y)).
linked((X,X),(X,X)):-node(X).

% SVG interaction
attr(edge,(X,Y),class,@svg_init("visibility","hidden")) :- edge((X,Y)).
attr(edge,E,class,@svg("click",X,"visibility","visible")):-linked(E,(X,Y)).
attr(edge,E,class,@svg("mouseenter",X,"opacity","1")):-linked(E,(X,Y)).
attr(edge,E,class,@svg("mouseleave",X,"opacity","0.2")):-linked(E,(X,Y)).

attr(node,X,class,@svg_init("visibility","hidden")):-node(X),jay!=X.
attr(node,Y,class,@svg("click",X,"visibility","visible")):-linked(E,(X,Y)).
attr(node,Y,class,@svg("mouseenter",X,"opacity","1")):-linked(E,(X,Y)).
attr(node,Y,class,@svg("mouseleave",X,"opacity","0.2")):-linked(E,(X,Y)).