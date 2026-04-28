% Interface
time(T):-true(_,T).
vertex((X,Y)) :- true(vertex((X,Y)),_).
edge((X,Y)) :- true(myedge(X,Y,D),_).
at(A,V,T) :- true(at(A,V),T).
move(A,(X,Y),T) :- true(move(A,X,Y),T).


moving(A,(X,Y),T) :- move(A,(X,Y),T).
moving(A,(X,Y),T) :- moving(A,(X,Y),T-1), not at(A,_,T), time(T).

vgraph(T):-time(T).
vattr(graph,T,bgcolor,gray):-time(T).
vattr(graph,T,pad,0):-time(T).
vattr(graph,T,margin,0):-time(T).
vattr(graph,T,label,T):-time(T).

vnode((V,T),T) :- vertex(V), time(T).
vedge(((X,T),(Y,T)),T) :- edge((X,Y)), time(T).
% vedge((X,Y)) :- edge((X,Y),D).

vattr(node,(V,T),width,"0.5") :- vertex(V), time(T).
% vattr(node,(V,T),margin,2) :- vertex(V), time(T).
% vattr(node,(V,T),fontname,"Computer Modern Sans"):- vertex(V), time(T).
vattr(node,(V,T),fontsize,10):- vertex(V), time(T).
vattr(node,(V,T),colorscheme,"ylgnbu9") :- vertex(V), time(T).
vattr(node,(V,T),shape,square) :- vertex(V), time(T).
vattr(node,(V,T),style,filled) :- vertex(V), time(T).
vattr(node,((X,Y),T),pos,@pos(X,Y)) :- vertex((X,Y)), time(T).

% vattr(node,(V,T),label,"<<FONT FACE='Computer Modern Serif'>{{value}}</FONT>>"):- vertex(V), time(T).
vattr(node,(V,T),fillcolor,A\8+1):- at(A,V,T), time(T).
vattr(node,(V,T),label,A):- at(A,V,T), time(T).
vattr(node,(V,T),label,""):- vertex(V), not at(_,V,T), time(T).
% vattr(node,(V,T),(label,value),@format("<I>s</I><SUB>{}</SUB> ",A)):- start(A,V), time(T).
% vattr(node,(V,T),(label,value),@format("<I>g</I><SUB>{}</SUB> ",A)):- goal(A,V), time(T).
% vattr(node,(V,T),fillcolor,A\8+1):- goal(A,V), not start(_,V), time(T).
% vattr(node,(V,T),fillcolor,white):- vertex(V), not goal(_,V), not start(_,V), time(T).
% vattr(node,(V,T),(label,value)," "):- vertex(V), not goal(_,V), not start(_,V), time(T).


vattr(edge,((X,T),(Y,T)),colorscheme,"ylgnbu9") :- edge((X,Y)), time(T).
vattr(edge,((X,T),(Y,T)),color,A\8+1) :- edge((X,Y)), moving(A,(X,Y),T), time(T).
