connection(X,Y,T):-connection(Y,X,T).
time(X,Y,T,C):-time(Y,X,T,C).

1 { cycle(X,Y,T) : connection(X,Y,T) } 1 :- city(X,_).
1 { cycle(X,Y,T) : connection(X,Y,T) } 1 :- city(Y,_).
reached(Y) :- cycle(S,Y,T),start(S).
reached(Y) :- cycle(X,Y,T), reached(X).
:- city(Y,_), not reached(Y).
#minimize {C,(X,Y) : cycle(X,Y,T),time(X,Y,T,C) }.