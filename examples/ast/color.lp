node(1..6).

edge(1,2). edge(1,3). edge(1,4). edge(2,4). edge(2,5).
edge(2,6). edge(3,4). edge(3,5). edge(5,6).

color(red; green; blue).

{ assign(N, C) : color(C) } = 1 :- node(N).
:- edge((N, M)), assign(N, C), assign(M, C).

#show node/1.
#show edge/1.
#show attr(node, N, style, filled): node(N).
#show attr(node, N, color, C) : assign(N, C).
