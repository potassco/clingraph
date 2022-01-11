
graph(program).

attr(graph_edges, program, dir, both).
attr(graph_edges, program, arrowtail, none).
attr(graph_edges, program, arrowhead, none).

node(atom_tuple(I)) :- atom_tuple(I).
attr(node, atom_tuple(E), shape, invhouse):- node(atom_tuple(E)).

node(literal_tuple(I)) :- literal_tuple(I).
attr(node, literal_tuple(E), shape, house):- node(literal_tuple(E)).

node(rule(H,B)):-rule(H,B).
attr(node, rule(H,B), shape, none):- node(rule(H,B)).

node(output(S,L)):- output(S,L).
attr(node, output(S,L), shape, underline):- node(output(S,L)).

node(atom(E)) :- literal_tuple(I,E), E>0.
node(atom(E)) :- atom_tuple(I,E), E>0.
attr(node, atom(E), shape, ellipse):- node(atom(E)).


% Atoms as part of an atom tuple
edge((atom_tuple(I),atom(E))):-atom_tuple(I,E).

% Positive atom in a literal tuple
edge((literal_tuple(I),atom(E))):-literal_tuple(I,E), E>0.
attr(edge, (literal_tuple(I),atom(E)), arrowhead, dot):-literal_tuple(I,E), E>0.

% Negative atom_tuple in a literal tuple
edge((literal_tuple(I),atom(-1*E))):-literal_tuple(I,E), E<0.
attr(edge, (literal_tuple(I),atom(-1*E)), arrowhead, odot):-literal_tuple(I,E), E<0.

% Literals as body of a rule
edge((rule(H,normal(B)),literal_tuple(B))):-rule(H,normal(B)).
attr(edge,(rule(H,normal(B)),literal_tuple(B)),arrowtail,normal):-rule(H,normal(B)).

% Atoms as choice head of a rule
edge((rule(choice(H),B),atom_tuple(H))):-rule(choice(H),B).
attr(edge,(rule(choice(H),B),atom_tuple(H)),arrowtail,oinv):-rule(choice(H),B).

% Atoms as disjuction head of a rule
edge((rule(disjunction(H),B),atom_tuple(H))):-rule(disjunction(H),B).
attr(edge,(rule(disjunction(H),B),atom_tuple(H)),arrowtail,inv):-rule(disjunction(H),B).

% Outputs
edge((literal_tuple(L),output(S,L))):-output(S,L).
attr(edge,(literal_tuple(L),output(S,L)),style,dotted):-output(S,L).
