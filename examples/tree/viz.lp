attr(node,X,style,"filled"):-node(X).
edge((X,Y)):-parent(X,Y).

linked_element(node,X,X):-node(X).
linked_element(node,Y,X):-edge((X,Y)).
linked_element(edge,(X,Y),X):-edge((X,Y)).


attr(node,X,class,@svg_init("visibility","hidden")):-node(X),not root(X).
attr(edge,(X,Y),class,@svg_init("visibility","hidden")) :- edge((X,Y)).


attr(Type,E,class,@svg("click",X,"visibility","visible")):-linked_element(Type,E,X).
attr(Type,E,class,@svg("mouseenter",X,"opacity","1")):-linked_element(Type,E,X).
attr(Type,E,class,@svg("mouseleave",X,"opacity","0.2")):-linked_element(Type,E,X).