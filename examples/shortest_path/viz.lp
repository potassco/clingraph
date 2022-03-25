node(X):-city(X).
edge((X,Y)):-road(X,Y,_).
attr(node,X,color,magenta):-start(X).
attr(node,X,color,magenta):-end(X).
attr(edge,(X,Y),label,S):-road(X,Y,S).
attr(edge,(X,Y),style,dotted):- not in_path(X,Y), road(X,Y,_).
attr(edge,(X,Y),color,magenta):- in_path(X,Y), road(X,Y,_).