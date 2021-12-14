% #const rate=1. % NOT IMPLEMENTED
#include "./action-MPP.lp".


ordered(order(O),product(A),N) :- init(object(order,O),  value(line,(A,N))).
shelved(shelf(S),product(A),N) :- init(object(product,A),value(on,  (S,N))), ordered(order(O),product(A)).

limit(A,O,S,(N+N'-|N-N'|)/2) :- ordered(O,A,N), shelved(S,A,N').

ordered(O,A,1..N,0) :- ordered(O,A,N).
shelved(S,A,1..N,0) :- shelved(S,A,N).



 { process(A,O,S,1..M,T) : limit(A,O,S,M) } 1 :- time(T).

process(A,O,M,T) :- process(A,O,_,M,T).
process(A,S,M,T) :- process(A,_,S,M,T).

process(A,shelf(S),T) :- process(A,shelf(S),M,T).
process(S,T)          :- process(A,S,T).

:- process(A,order(O),M,T), not ordered(order(O),A,M,T-1).
:- process(A,shelf(S),M,T), not shelved(shelf(S),A,M,T-1).

ordered(O,A,N-M,T) :- ordered(O,A,N,T-1), process(A,O,M,T), M < N.
shelved(S,A,N-M,T) :- shelved(S,A,N,T-1), process(A,S,M,T), M < N.

ordered(O,A,N,  T) :- ordered(O,A,N,T-1), not process(A,O,_,T), time(T).
shelved(S,A,N,  T) :- shelved(S,A,N,T-1), not process(A,S,T), time(T).

:- process(_,O,S,_,T), target(O,P), position(P,C), not position(S,C,T-1).


:- process(S,T), not carries(_,S,T-1).
:- process(S,T), carries(R,S,T-1), not waits(R,T).
