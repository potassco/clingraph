#include "./quantities.lp".



:- ordered(_,_,1,horizon).

:- carries(_,_,horizon).

:- position(_,C), position(_,C,horizon).
