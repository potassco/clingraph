node(X):-person(X).
edge((X,Y,L)):-link(X,Y,L).
attr(edge,(X,Y,L),label,L):-link(X,Y,L).
attr(edge,(X,Y,L),fontsize,10):-link(X,Y,L).