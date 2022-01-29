
graph(system).
attr(graph,system,nodesep,"3").
node(start,system).
attr(node,start,texlbl,"start").
attr(node,start,shape,none).
edge((start,Q)):-initial_state(Q).
attr(edge,(start,Q),arrowhead,vee):-initial_state(Q).

attr(graph_nodes,system,shape,circle).
attr(graph_nodes,system,width,"1").
attr(graph_nodes,system,hight,"1").

attr(graph_edges,system,style,dotted).
node(Q,system):-state(Q).

attr(node,green,label,"green"):-state(green).
attr(node,green,texlbl,"$\\triangleright$"):-state(green).
attr(node,green,color,green):-state(green).

attr(node,yellow,label,"yellow"):-state(yellow).
attr(node,yellow,texlbl,"$\\sim$"):-state(yellow).
attr(node,yellow,color,yellow):-state(yellow).

attr(node,red,label,"red"):-state(red).
attr(node,red,texlbl,"$\\otimes$"):-state(red).
attr(node,red,color,red):-state(red).


edge((X,Z),system):-transition(X,Y,Z).
attr(edge,(X,Z),label,Z):-transition(X,Y,Z).
attr(edge,(X,Z),(texlbl,0),"$\\mathcal{C}_{\\textit{"):-transition(X,Y,Z).
attr(edge,(X,Z),(texlbl,1),Z):-transition(X,Y,Z).
attr(edge,(X,Z),(texlbl,2),"}}$"):-transition(X,Y,Z).