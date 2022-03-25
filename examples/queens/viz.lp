#script (python)
from clingo.symbol import String
def pos(x,y):
    return String(f"{str(x)},{str(y)}!")
#end.

node((X,Y)):-cell(X,Y).
attr(node,(X,Y),width,1):-cell(X,Y).
attr(node,(X,Y),shape,square):-cell(X,Y).
attr(node,(X,Y),pos,@pos(X,Y)):-cell(X,Y).
attr(node,(X,Y),style,filled):-cell(X,Y).
attr(node,(X,Y),fillcolor,gray):-cell(X,Y),(X+Y)\2=0.
attr(node,(X,Y),fillcolor,white):-cell(X,Y),(X+Y)\2!=0.
attr(node,(X,Y),label,"♕"):-queen(X,Y).
attr(node,(X,Y),fontsize,"50"):-queen(X,Y).


% attr(node,(X,Y),(pos,0),X):-cell(X,Y).
% attr(node,(X,Y),(pos,1),","):-cell(X,Y).
% attr(node,(X,Y),(pos,2),Y):-cell(X,Y).
% attr(node,(X,Y),(pos,3),"!"):-cell(X,Y).
% attr(node,(X,Y),(pos,sep),""):-cell(X,Y).