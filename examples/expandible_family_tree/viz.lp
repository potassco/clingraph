node(X):-person(X).
edge((X,Y)):-parent(X,Y).
attr(graph,default,label,"Modern Family Tree (click on the nodes to expand)"):-edge((X,Y)).
attr(edge,(X,Y),class,"expandible"):-edge((X,Y)).
attr(edge,(X,Y),class,"hidden"):-edge((X,Y)).
attr(edge,(X,Y),class,X):-related(X,Y).
attr(edge,(Y,X),class,X):-related(X,Y).
attr(node,X,style,"filled"):-node(X).
attr(node,X,class,"expandible"):-node(X).
attr(node,X,class,"hidden"):-node(X),jay!=X.
attr(node,Y,class,X):-related(X,Y).
attr(node,X,id,X):-node(X).