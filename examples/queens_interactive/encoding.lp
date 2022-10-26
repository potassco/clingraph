#const n=5.
cell(1..n,1..n).
1 { queen(I,1..n) } 1 :- I = 1..n.
1 { queen(1..n,J) } 1 :- J = 1..n.
 :- 2 { queen(D-J,J) }, D = 2..2*n.
 :- 2 { queen(D+J,J) }, D = 1-n..n-1.