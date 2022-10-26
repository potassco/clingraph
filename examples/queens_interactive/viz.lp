#const n=5.

node((X,Y)) :- cell(X,Y).

attr(node,(X,Y),id,(X,Y)) :- cell(X,Y).
attr(node,(X,Y),overlap,true) :- cell(X,Y).
attr(node,(X,Y),sep) :- cell(X,Y).
attr(node,(X,Y),esep) :- cell(X,Y).
attr(node,(X,Y),width,1) :- cell(X,Y).
attr(node,(X,Y),shape,square) :- cell(X,Y).
attr(node,(X,Y),style,filled) :- cell(X,Y).
attr(node,(X,Y),fillcolor,gray) :- cell(X,Y),(X+Y)\2 = 0.
attr(node,(X,Y),fillcolor,white) :- cell(X,Y),(X+Y)\2 != 0.
attr(node,(X,Y),fontsize,"50") :- queen(X,Y).
attr(node,(X,Y),label,"♕") :- queen(X,Y).
attr(node,(X,Y),pos,@pos(X,Y)) :- cell(X,Y).

% Interaction
dir(-1..1,-1..1).
attack((QX,QY),(X,Y)):- queen(QX,QY), cell(X,Y), D=1..n, dir(DX,DY), X==QX+(DX*D), Y==QY+(DY*D).
node(a(Q,C)) :- attack(Q,C).
attr(node,a(Q,C),id,a(Q,C)) :- attack(Q,C).
attr(node,a(Q,C),width,1) :- attack(Q,C).
attr(node,a(Q,C),shape,square) :- attack(Q,C).
attr(node,a(Q,C),style,filled) :- attack(Q,C).
attr(node,a(Q,C),fillcolor,red) :- attack(Q,C).
attr(node,a(Q,(X,Y)),fontsize,"50") :- queen(X,Y), attack(Q,(X,Y)).
attr(node,a(Q,(X,Y)),label,(X,Y)) :- attack(Q,(X,Y)), not queen(X,Y).
attr(node,a(Q,(X,Y)),label,"♕") :- queen(X,Y), attack(Q,(X,Y)).
attr(node,a(Q,(X,Y)),pos,@pos(X,Y)) :- attack(Q,(X,Y)).
attr(node,a(Q,C),class,"hidden") :- attack(Q,C).
attr(node,a(Q,C),class,@concat("mouseenter_",Q,"_visible")) :- attack(Q,C).
attr(node,a(Q,C),class,@concat("mouseleave_",Q,"_hidden")) :- attack(Q,C).
attr(node,C,class,@concat("mouseenter_",Q,"_hidden")) :- attack(Q,C).
attr(node,C,class,@concat("mouseleave_",Q,"_visible")) :- attack(Q,C).
