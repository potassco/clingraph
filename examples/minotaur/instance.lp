%
% Instance
%

field(1..3,1..3).
start(2,1).
goal(3,2).
mino(2,3).
wall(2,1,2,2). wall(2,2,3,2). wall(2,2,2,3).
wall(X,Y,XX,YY) :- wall(XX,YY,X,Y).
maxsteps(10).

