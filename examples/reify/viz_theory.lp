
% Symbols

% theory_number(I,N).
% theory_string(I,S).
% theory_function(I,S,T).
% theory_sequence(I,tuple,T).


node(theory_symbol(I)):-theory_number(I,N).
node(theory_symbol(I)):-theory_string(I,S).
node(theory_symbol(I)):-theory_function(I,S,T).
node(theory_symbol(I)):-theory_sequence(I,tuple,T).
theory_node(theory_symbol(I)):-theory_number(I,N).
theory_node(theory_symbol(I)):-theory_string(I,S).
theory_node(theory_symbol(I)):-theory_function(I,S,T).
theory_node(theory_symbol(I)):-theory_sequence(I,tuple,T).

attr(node,theory_symbol(I),label,theory_number(N)):-theory_number(I,N).
attr(node,theory_symbol(I),label,theory_string(S)):-theory_string(I,S).
attr(node,theory_symbol(I),label,theory_function(I)):-theory_function(I,S,T).
attr(node,theory_symbol(I),label,theory_sequence(I)):-theory_sequence(I,tuple,T).

attr(node,theory_symbol(I),shape,note):-node(theory_symbol(I)).

edge((theory_symbol(I),theory_tuple(T))):-theory_function(I,S,T).
edge((theory_symbol(I),theory_symbol(S))):-theory_function(I,S,T).
attr(edge,(theory_symbol(I),theory_symbol(S)),arrowhead,odiamond):-theory_function(I,S,T).


% Tuples

node(theory_tuple(I)):-theory_tuple(I).
theory_node(theory_tuple(I)):-theory_tuple(I).
attr(node, theory_tuple(I), shape, house):-theory_tuple(I).
edge((theory_tuple(I),theory_symbol(E))):-theory_tuple(I,P,E).
attr(edge,(theory_tuple(I),theory_symbol(E)),label,P):-theory_tuple(I,P,E).


% Elements
node(theory_element(I)):-theory_element(I,T,C).
theory_node(theory_element(I)):-theory_element(I,T,C).
attr(node,theory_element(I),shape, invtrapezium):-theory_element(I,T,C).
edge((theory_element(I),theory_tuple(T))):-theory_element(I,T,C).
edge((theory_element(I),literal_tuple(C))):-theory_element(I,T,C), C!=true.
attr(edge,(theory_element(I),literal_tuple(C)),arrowtail,curve):-theory_element(I,T,C), C!=true.


node(theory_element_tuple(I)):-theory_element_tuple(I).
attr(node,theory_element_tuple(I),shape,house):-theory_element_tuple(I,ET).
theory_node(theory_element_tuple(I)):-theory_element_tuple(I,ET).
edge((theory_element_tuple(I),theory_element(ET))):-theory_element_tuple(I,ET).

% Atom

node(atom(I)):-theory_atom(I,S,ET).
theory_node(atom(I)):-theory_atom(I,S,ET).
attr(node,atom(I),label,theory_atom(I)):-theory_atom(I,S,ET).
edge((atom(I),theory_element_tuple(ET))):-theory_atom(I,S,ET).
edge((atom(I),theory_symbol(S))):-theory_atom(I,S,ET).
attr(edge,(atom(I),theory_symbol(S)),arrowhead,odiamond):-theory_atom(I,S,ET).
% theory_atom(I,S,ET,G,S).



attr(node,N,style,filled):-theory_node(N).
attr(node,N,fillcolor,"#ECD9F0"):-theory_node(N).