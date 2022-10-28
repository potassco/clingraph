
% ---- Auxiliary predicates
color(1,blue). color(2,green). color(3,red). color(4,blue4). 
color(5,brown4). color(6,orange). color(7,yellow). color(8,pink). 

opens(C,C):-cell(C).
opens(C,C'):-cell(C),mine(C),cell(C').
opens(C,C'):-cell(C),count(C,0),adjacent(C,C').
opens(C,C''):-cell(C),count(C,0),adjacent(C,C'),opens(C',C'').

% ---- Graph
attr(graph,default,label,"Minesweeper").
attr(graph,default,(label,0), "     Find "):-n_mines(N).
attr(graph,default,(label,1), N):-n_mines(N).
attr(graph,default,(label,2), "mines"):-n_mines(N).
attr(graph,default,fontname,"Copperplate").

% --- Nodes (Notice this are three grids one on top of another)
node(C):-cell(C).
node(hide(C)):-cell(C).
node(flag(C)):-cell(C).
attr(node,C,id,C) :- node(C). %Needed for inteactivity

% Common style
attr(node,C,fontsize,20):-node(C).
attr(node,N,width,"0.5") :- node(N).
attr(node,N,shape,square) :- node(N).
attr(node,N,style,filled) :- node(N).
attr(node,N,fontname,"Copperplate") :- node(N).
attr(node,C,color,"gray35"):-node(C).
attr(node,C,penwidth,2):-node(C).

% Pos 
attr(node,(X,Y),pos,@pos(X,Y,"0.5")):-cell((X,Y)).
attr(node,hide((X,Y)),pos,@pos(X,Y,"0.5")):-cell((X,Y)).
attr(node,flag((X,Y)),pos,@pos(X,Y,"0.5")):-cell((X,Y)).

% Label 
attr(node,C,label,"⚈"):-mine(C).
attr(node,C,label,N):-count(C,N),not mine(C),N!=0.
attr(node,C,label,""):-count(C,0),not mine(C).
attr(node,hide(C),label,"") :- cell(C).
attr(node,flag(C),label,"⚑") :- cell(C).

% Color
attr(node,C,fontcolor,Color):-count(C,N),N!=0,not mine(C),color(N,Color).
attr(node,hide(C),fillcolor,"gray90:gray80"):-cell(C).
attr(node,flag(C),fillcolor,"gray90:gray80"):-cell(C).
attr(node,hide(C),gradientangle,315):-cell(C).
attr(node,C,fillcolor,"gray65"):-cell(C).


% Interactivity
attr(node,C,class,@svg_init("visibility","hidden")):-cell(C).
attr(node,flag(C),class,@svg_init("visibility","hidden")):-cell(C).
attr(node,flag(C),class,@svg("contextmenu",hide(C),"visibility","visible")):-cell(C).
attr(node,hide(C),class,@svg("contextmenu",hide(C),"visibility","hidden")):-cell(C).
attr(node,C,class,@svg("contextmenu",hide(C),"visibility","hidden")):-cell(C).
attr(node,flag(C),class,@svg("contextmenu",flag(C),"visibility","hidden")):-cell(C).
attr(node,C,class,@svg("contextmenu",flag(C),"visibility","visible")):-cell(C).
attr(node,C',class,@svg("click",hide(C),"visibility","visible")):-opens(C,C').
attr(node,hide(C'),class,@svg("click",hide(C),"visibility","hidden")):-opens(C,C').