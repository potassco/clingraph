related(X,Y):-parent(X,Y).
related(Y,X):-parent(X,Y).
related(X,X):-person(X).

node(X):-person(X).
attr(node,X,label,@stringify(X,true)):-person(X).
attr(node,X,style,"filled"):-node(X).
edge((X,Y)):-parent(X,Y).

attr(graph,default,label,"Modern Family Tree (click on the nodes to expand)"):-edge((X,Y)).

root(jay).
linked_element(node,Y,X):-related(X,Y).
linked_element(edge,(X,Y),X):-related(X,Y),edge((X,Y)).
linked_element(edge,(Y,X),X):-related(X,Y),edge((Y,X)).


% SVG interaction
attr(edge,E,class,@svg_init("visibility","hidden")) :- edge(E).
attr(node,X,class,@svg_init("visibility","hidden")):-node(X),not root(X).

attr(Type,E,class,@svg("click",X,"visibility","visible")):-linked_element(Type,E,X).
attr(Type,E,class,@svg("mouseenter",X,"opacity","1")):-linked_element(Type,E,X).
attr(Type,E,class,@svg("mouseleave",X,"opacity","0.2")):-linked_element(Type,E,X).