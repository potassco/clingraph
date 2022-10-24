node(X):-person(X).
edge((X,Y,L,1)):-link(X,Y,L).
attr(edge,(X,Y,L,1),label,L):-link(X,Y,L).
attr(edge,(X,Y,L,1),fontsize,10):-link(X,Y,L).