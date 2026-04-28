vnode((X,Y)) :- vertex((X,Y)).
% edge((X,Y)) :- edge(X,Y).
% vedge((X,Y)) :- edge((X,Y),D).
vattr(graph,default,bgcolor,black).
vattr(graph,default,pad,0).
vattr(graph,default,margin,0).

vattr(node,V,width,1) :- vertex(V).
% vattr(node,V,fontname,"Computer Modern Sans"):- vertex(V).
vattr(node,V,fontsize,22):- vertex(V).
vattr(node,V,colorscheme,"ylgnbu9") :- vertex(V).
vattr(node,V,shape,square) :- vertex(V).
vattr(node,V,style,filled) :- vertex(V).
vattr(node,(X,Y),pos,@pos(X,Y)) :- vertex((X,Y)).

vattr(node,V,label,"<<FONT FACE='Computer Modern Serif'>{{value}}</FONT>>"):- vertex(V).
vattr(node,V,(label,value),@format("<I>s</I><SUB>{}</SUB> ",A)):- start(A,V).
vattr(node,V,fillcolor,A\8+1):- start(A,V).
vattr(node,V,(label,value),@format("<I>g</I><SUB>{}</SUB> ",A)):- goal(A,V).
vattr(node,V,fillcolor,A\8+1):- goal(A,V), not start(_,V).
vattr(node,V,fillcolor,white):- vertex(V), not goal(_,V), not start(_,V).
vattr(node,V,(label,value)," "):- vertex(V), not goal(_,V), not start(_,V).
