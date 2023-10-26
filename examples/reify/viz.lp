#const pos_body_lit_color= @color(green).
#const neg_body_lit_color= @color(red).
#const tab_color= @color(yellow,50).
#const rule_color = @color(blue,50).
#const external_color = @color(green,70).
#const atom_color = @color(gray,50).
#const theory_symbol_color = @color(purple,50).

#defined atom_tuple/1.
#defined atom_tuple/2.
#defined literal_tuple/1.
#defined literal_tuple/2.
#defined output/2.
#defined theory_number/2.
#defined theory_string/2.
#defined theory_function/3.
#defined theory_atom/3.
#defined theory_atom/5.
#defined theory_tuple/1.
#defined theory_tuple/3.
#defined theory_sequence/3.

atom(E, atom_tuple(A,E)):- atom_tuple(A,E), E>0.
atom(E, external(E,V)):- external(E,V).
atom(E, theory_atom(E,S,ET)):- theory_atom(E,S,ET).%Theory atom without guard
atom(E, theory_atom(E,S,ET,ID_G,ID_S)):- theory_atom(E,S,ET,ID_G,ID_S).%Theory atom with guard
node(P):-atom(E,P).
attr(node, P, shape, box):- atom(E, P).
attr(node, P, fillcolor, atom_color):- atom(E, P).
attr(node, P, (label,value), S):- atom(E, P), literal_tuple(L,E), output(S,L).

attr(node, N, fillcolor, tab_color):- attr(node, N, shape, tab).

theory(theory_atom(E,S,ET)) :- node(theory_atom(E,S,ET)).
theory(theory_atom(E,S,ET,ID_G,ID_S)) :- node(theory_atom(E,S,ET,ID_G,ID_S)).
theory(theory_element(I,T,C)) :- node(theory_element(I,T,C)).
theory(theory_element_tuple(I)) :- node(theory_element_tuple(I)).
theory(theory_tuple(I)) :- node(theory_tuple(I)).
theory(N) :- theory_any_symbol(I,N).
attr(node, N, fontcolor, "#6A6A6A"):- theory(N).
attr(node, N, color, "#6A6A6A"):- theory(N).

attr(graph_edges, default, dir, both).
attr(graph_edges, default, arrowtail, none).
attr(graph_edges, default, arrowhead, none).

attr(node,N,label,"<{{name}}{% if value is defined %} <br/><br/> <FONT POINT-SIZE='15pt'> <i><b>{{value}} </b></i></FONT> {% else %} {% endif %}>") :- node(N).
attr(node,N,(label,name),N) :- node(N).
attr(node,N,style,filled) :- node(N), not attr(node,N,shape,plaintext).
attr(edge,(N1,N2),fontsize,8):-edge((N1,N2)).


node(atom_tuple(I)) :- atom_tuple(I).
attr(node, atom_tuple(E), shape, tab):- node(atom_tuple(E)).

node(literal_tuple(I)) :- literal_tuple(I).
attr(node, literal_tuple(E), shape, tab):- node(literal_tuple(E)).

% Internal atoms 


node(rule(H,B)):-rule(H,B).
attr(node,rule(H,B),shape,box) :- node(rule(H,B)).
attr(node,rule(H,B),fillcolor,rule_color) :- node(rule(H,B)).


node(output(S,L)):- output(S,L).
attr(node, output(S,L), shape, plaintext):- node(output(S,L)).
attr(node, output(S,L), (label,value), S):- node(output(S,L)).

node(atom_tuple(A,E)) :- literal_tuple(I,E), E>0, atom_tuple(A,E).
node(atom_tuple(I,E)) :- atom_tuple(I,E), E>0.
attr(node, P, shape, box):- atom(E,P).
attr(node, P, (label,value), S):- atom(E,P), literal_tuple(L,E), output(S,L).


attr(node,external(E,V),fillcolor,external_color) :- node(external(E,V)).


% Atoms as part of an atom tuple
edge((atom_tuple(I),A)):-atom_tuple(I,E), atom(E,A).

% edge((atom_tuple(I),atom_tuple(I,E))):-atom_tuple(I,E).

% Positive atom in a literal tuple
edge((literal_tuple(I),P)):-literal_tuple(I,E), E>0, atom(E,P).
attr(edge, (literal_tuple(I),P), color, pos_body_lit_color):-literal_tuple(I,E), E>0, atom(E,P).
attr(edge, (literal_tuple(I),P), label, literal_tuple(I,E)):-literal_tuple(I,E), E>0, atom(E,P).
attr(edge, (literal_tuple(I),P), arrowhead, dot):-literal_tuple(I,E), E>0, atom(E,P).

% Negative atom_tuple in a literal tuple
edge((literal_tuple(I),P)):-literal_tuple(I,E), E<0, atom(-1*E,P).
attr(edge, (literal_tuple(I),P), color, neg_body_lit_color):-literal_tuple(I,E), E<0, atom(-1*E,P).
attr(edge, (literal_tuple(I),P), arrowhead, dot):-literal_tuple(I,E), E<0, atom(-1*E,P).

% Literals as body of a rule
edge((rule(H,normal(B)),literal_tuple(B))):-rule(H,normal(B)).
attr(edge,(rule(H,normal(B)),literal_tuple(B)),label,"body"):-rule(H,normal(B)).

% Atoms as choice head of a rule
edge((rule(choice(H),B),atom_tuple(H))):-rule(choice(H),B).
attr(edge,(rule(choice(H),B),atom_tuple(H)),label,"head"):-rule(choice(H),B).
% attr(edge,(rule(choice(H),B),atom_tuple(H)),arrowtail,oinv):-rule(choice(H),B).

% Atoms as disjuction head of a rule
edge((rule(disjunction(H),B),atom_tuple(H))):-rule(disjunction(H),B).
attr(edge,(rule(disjunction(H),B),atom_tuple(H)),label,"head"):-rule(disjunction(H),B).

% Outputs
edge((literal_tuple(L),output(S,L))):-output(S,L).
attr(edge,(literal_tuple(L),output(S,L)),style,dotted):-output(S,L).




% -------- Theory

theory_any_symbol(I,theory_number(I,N)):-theory_number(I,N).
theory_any_symbol(I,theory_string(I,@html_escape(S))):-theory_string(I,S).
theory_any_symbol(I,theory_function(I,S,T)):-theory_function(I,S,T).
theory_any_symbol(I,theory_sequence(I,tuple,T)):-theory_sequence(I,tuple,T).

node(N):-theory_any_symbol(I,N).
attr(node,N,fillcolor,theory_symbol_color):-theory_any_symbol(I,N).

attr(node,theory_string(I,S),shape,plaintext):-theory_any_symbol(I,theory_string(I,S)).
attr(node,theory_string(I,S),(label,value),S):-theory_any_symbol(I,theory_string(I,S)).

attr(node,theory_number(I,N),shape,plaintext):-theory_any_symbol(I,theory_number(I,N)).
attr(node,theory_number(I,N),(label,value),N):-theory_any_symbol(I,theory_number(I,N)).


edge((N,theory_tuple(T))):-theory_function(I,S,T), theory_any_symbol(I,N).
edge((N,SN)):-theory_function(I,S,T), theory_any_symbol(I,N), theory_any_symbol(S,SN).

% Tuples

node(theory_tuple(I)):-theory_tuple(I).
attr(node,theory_tuple(I),shape,tab):-theory_tuple(I).
edge((theory_tuple(I),N)):-theory_tuple(I,P,E), theory_any_symbol(E,N).
attr(edge,(theory_tuple(I),N),label,theory_tuple(I,P,E)):-theory_tuple(I,P,E), theory_any_symbol(E,N).


% Elements
node(theory_element(I,T,C)):-theory_element(I,T,C).
attr(node,theory_element(I,T,C), fillcolor, theory_symbol_color ):-theory_element(I,T,C).
edge((theory_element(I,T,C),theory_tuple(T))):-theory_element(I,T,C).
edge((theory_element(I,T,C),literal_tuple(C))):-theory_element(I,T,C), C!=true.
attr(edge,(theory_element(I,T,C),literal_tuple(C)),label,condition):-theory_element(I,T,C), C!=true.


node(theory_element_tuple(I)):-theory_element_tuple(I).
attr(node,theory_element_tuple(I),shape,tab):-theory_element_tuple(I).
edge((theory_element_tuple(I),theory_element(ET,T,C))):-theory_element_tuple(I,ET), theory_element(ET,T,C).


% Atom
edge((theory_atom(I,S,ET),theory_element_tuple(ET))):-theory_atom(I,S,ET).
attr(edge,(theory_atom(I,S,ET),theory_element_tuple(ET)),label,element):-theory_atom(I,S,ET).
edge((theory_atom(I,S,ET),SN)):-theory_atom(I,S,ET), theory_any_symbol(S,SN).
attr(edge,(theory_atom(I,S,ET),SN),label,name):-theory_atom(I,S,ET), theory_any_symbol(S,SN).

edge((theory_atom(E,S,ET,ID_G,ID_S),theory_element_tuple(ET))):-theory_atom(E,S,ET,ID_G,ID_S).
attr(edge,(theory_atom(E,S,ET,ID_G,ID_S),theory_element_tuple(ET)),label,element):-theory_atom(E,S,ET,ID_G,ID_S).
edge((theory_atom(E,S,ET,ID_G,ID_S),SN)):-theory_atom(E,S,ET,ID_G,ID_S), theory_any_symbol(S,SN).
attr(edge,(theory_atom(E,S,ET,ID_G,ID_S),SN),label,name):-theory_atom(E,S,ET,ID_G,ID_S), theory_any_symbol(S,SN).
edge((theory_atom(E,S,ET,ID_G,ID_S),SN)):-theory_atom(E,S,ET,ID_G,ID_S), theory_any_symbol(ID_S,SN).
attr(edge,(theory_atom(E,S,ET,ID_G,ID_S),SN),label,right):-theory_atom(E,S,ET,ID_G,ID_S), theory_any_symbol(ID_S,SN).
edge((theory_atom(E,S,ET,ID_G,ID_S),SG)):-theory_atom(E,S,ET,ID_G,ID_S), theory_any_symbol(ID_G,SG).
attr(edge,(theory_atom(E,S,ET,ID_G,ID_S),SG),label,guard):-theory_atom(E,S,ET,ID_G,ID_S), theory_any_symbol(ID_G,SG).

