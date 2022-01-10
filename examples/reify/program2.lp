#theory theory{
    term {
	 >   : 2, unary;
	 >?  : 1, binary, left
	 };
    &tel/0     : term, any;
    &tel_eq/0     : term, {=}, term, any
}.

:- &tel{ > f(a,1) }, a.
{a}.


% atom_tuple(0).
% atom_tuple(0,1).
% literal_tuple(0).
% rule(choice(0),normal(0)).
% atom_tuple(1).
% literal_tuple(1).
% literal_tuple(1,1).
% literal_tuple(1,2).
% rule(disjunction(1),normal(1)).
% theory_string(0,"tel").
% theory_string(3,"a").
% theory_number(4,1).
% theory_string(2,"f").
% theory_tuple(0).
% theory_tuple(0,0,3).
% theory_tuple(0,1,4).
% theory_function(5,2,0).
% theory_string(1,">").
% theory_tuple(1).
% theory_tuple(1,0,5).
% theory_function(6,1,1).
% theory_tuple(2).
% theory_tuple(2,0,6).
% theory_element(0,2,0).
% theory_element_tuple(0).
% theory_element_tuple(0,0).
% theory_atom(2,0,0).
% literal_tuple(2).
% literal_tuple(2,1).
% output(a,2). 
