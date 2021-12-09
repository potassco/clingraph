node(1..6).

edge(
    1,2; 1,3; 1,4;
    2,4; 2,5; 2,6;
    3,4; 3,5;
    5,6
).

color(red; green; blue).

{ assign(N, C) : color(C) } = 1 :- node(N).

:- edge(N, M), assign(N, C), assign(M, C).

#show type(graph).
#show node/1.
#show edge/2.
#show attr(N, color, C) : assign(N, C).
