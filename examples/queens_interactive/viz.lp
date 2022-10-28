#const n=5.

node((X,Y)) :- cell(X,Y).

attr(node,(X,Y),id,(X,Y)) :- cell(X,Y).
attr(node,(X,Y),overlap,true) :- cell(X,Y).
attr(node,(X,Y),sep) :- cell(X,Y).
attr(node,(X,Y),esep) :- cell(X,Y).
attr(node,(X,Y),width,1) :- cell(X,Y).
attr(node,(X,Y),shape,square) :- cell(X,Y).
attr(node,(X,Y),style,filled) :- cell(X,Y).
attr(node,(X,Y),fillcolor,@svg_color()) :- cell(X,Y),(X+Y)\2 = 0.
attr(node,(X,Y),fillcolor,@svg_color()) :- cell(X,Y),(X+Y)\2 != 0.
attr(node,(X,Y),fontsize,"50") :- queen(X,Y).
attr(node,(X,Y),label,"♕") :- queen(X,Y).
attr(node,(X,Y),pos,@pos(X,Y)) :- cell(X,Y).

% Interaction
dir(-1..1,-1..1).
attack((QX,QY),(X,Y)):- queen(QX,QY), cell(X,Y), D=1..n, dir(DX,DY), X==QX+(DX*D), Y==QY+(DY*D).
attr(node,(X,Y),class,@svg_init("color","gray")) :- attack(Q,(X,Y)), (X+Y)\2 != 0.
attr(node,(X,Y),class,@svg_init("color","white")) :- attack(Q,(X,Y)), (X+Y)\2 == 0.
attr(node,C,class,@svg("mouseenter",Q,"color","red")) :- attack(Q,C).
attr(node,(X,Y),class,@svg("mouseleave",Q,"color","gray")) :- attack(Q,(X,Y)), (X+Y)\2 != 0.
attr(node,(X,Y),class,@svg("mouseleave",Q,"color","white")) :- attack(Q,(X,Y)), (X+Y)\2 == 0.
