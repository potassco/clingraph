
position(R,(X,Y),T) :- positionX(R,X,T), positionY(R,Y,T).
:- highway(C), not carries(_,S,T), position(S,C,T), isShelf(S).
:- highway(C),         waits(R,T), position(R,C,T).
