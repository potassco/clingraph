#theory theory{
    term {
	 >   : 2, unary;
	 >?  : 1, binary, left
	 };
    &tel/0     : term, any;
    &tel_eq/0     : term, {=}, term, any
}.

:- &tel{ > f(a,1) }, c.
{a}.

#show f(a,1) : &tel{ > f(a,1) }.
#external c.
