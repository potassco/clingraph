#const n = 7.
#const n_mines = 10.

n_mines(n_mines).
cell((0..n,0..n)).

{mine(C)}:-cell(C).
:- #count{C:mine(C)}!= n_mines.
dir(-1..1).
adjacent((X,Y),(X+DX,Y+DY)):-cell((X,Y)), cell((X+DX,Y+DY)), dir(DX), dir(DY).
count((X,Y),N):- #sum{1,X',Y':mine((X',Y')),adjacent((X,Y),(X',Y'))}=N, cell((X,Y)).