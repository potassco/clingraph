
%%%%%%%%%%%% Legend
graph(legend,program).
attr(graph, legend, label, "LEGEND").
attr(graph, legend, fontsize, "20").
attr(graph,legend,style,filled).
attr(graph,legend,fillcolor,gray).

graph(legend1,legend).
attr(graph, legend1, label, "Literal tuples (Bodys)").
node(literal_tuple,legend1).
node(positive_atom,legend1).
node(negative_atom,legend1).
attr(node, literal_tuple, shape, house).
attr(node, positive_atom, shape, ellipse).
attr(node, negative_atom, shape, ellipse).
attr(edge,(literal_tuple,positive_atom),arrowhead,dot).
attr(edge,(literal_tuple,negative_atom),arrowhead,odot).
node(literal_tuple_meaning,legend1).
attr(node,literal_tuple_meaning,shape, plaintext).
attr(node,literal_tuple_meaning,label, "A set of literals defined as the conjuction \\n of positive and negative atoms").

graph(legend2,legend).
attr(graph, legend2, label, "Atoms tuples (Heads)").
node(atom_tuple,legend2).
attr(node, atom_tuple, shape, invhouse).
node(atom_tuple_meaning,legend2).
attr(node,atom_tuple_meaning,shape, plaintext).
attr(node,atom_tuple_meaning,label, "A set of atoms defined as \\n the disjuction or choice among atoms").


graph(legend3,legend).
attr(graph, legend3, label, "Atoms").
node(atom,legend3).
attr(node, atom, shape, ellipse).
node(atom_meaning,legend3).
attr(node,atom_meaning,shape, plaintext).
attr(node,atom_meaning,label, "An atom").

graph(legend4,legend).
attr(graph, legend4, label, "Rules").
node(rule,legend4).
node(rule_head,legend4).
node(rule_body,legend4).
attr(node, rule, shape, rectangle).
attr(node, rule_head, shape, invhouse).
attr(node, rule_body, shape, house).

attr(edge,(rule,rule_body),arrowtail,normal).
attr(edge,(rule,rule_head),arrowtail,inv).
node(rule_meaning,legend4).
attr(node,rule_meaning,shape, plaintext).
attr(node,rule_meaning,label, "An rule defined by a \\n head  which is a choice or a disjuction of atoms (pointing to an atom tuple)\\n and a body which is a conjuction of literals (pointing to a literal_tuple)").

graph(legend5,legend).
attr(graph, legend5, label, "Output").
node(output,legend5).
node(literal_outpt,legend5).
attr(node, output, shape, underline).
attr(node, literal_outpt, shape, house).

attr(edge,(output,literal_outpt),style,dotted).
node(out_meaning,legend5).
attr(node,out_meaning,shape, plaintext).
attr(node,out_meaning,label, "An output that will be printed when the \\n literals from the literal_tuple hold").

attr(graph,X,style,dotted):-graph(X,legend).