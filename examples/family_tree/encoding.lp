cupple(jay,gloria).

parent(jay,joe).
parent(gloria,joe).

parent(javier,manny).
parent(gloria,manny).
parent(javier,manny).

parent(jay,mitchel).
parent(dede,mitchel).
parent(jay,claire).
parent(dede,claire).

cupple(phil,claire).

parent(claire,haley).
parent(phil,haley).
parent(claire,alex).
parent(phil,alex).
parent(claire,luke).
parent(phil,luke).

cupple(dylan,haley).
parent(dylan,george).
parent(haley,george).
parent(dylan,poppy).
parent(haley,poppy).
cupple(cameron,mitchel).
parent(cameron,lily).
parent(mitchel,lily).
parent(cameron,rex).
parent(mitchel,rex).


person(X):-parent(X,_).
person(X):-parent(_,X).
person(X):-cupple(X,_).
person(X):-cupple(_,X).

related(X,Y):-parent(X,Y).
related(X,Y):-parent(Y,X).
