node(X):-person(X).
edge((X,Y)):-parent(X,Y).
attr(graph,default,label,"Modern Family Tree (click on the nodes to expand)"):-edge((X,Y)).
attr(edge,(X,Y),class,"hidden"):-edge((X,Y)).
attr(edge,(X,Y),class,@concat("click_",X,"_visible")):-parent(X,Y).
attr(edge,(X,Y),class,@concat("mouseenter_",X,"_focus")):-parent(X,Y).
attr(edge,(X,Y),class,@concat("mouseleave_",X,"_blur")):-parent(X,Y).
attr(edge,(X,Y),class,@concat("click_",Y,"_visible")):-parent(X,Y).
attr(edge,(X,Y),class,@concat("mouseenter_",Y,"_focus")):-parent(X,Y).
attr(edge,(X,Y),class,@concat("mouseleave_",Y,"_blur")):-parent(X,Y).
attr(node,X,style,"filled"):-node(X).
attr(node,X,id,X):-node(X). %Needed to referenciate the nodes in the svg file!
attr(node,X,class,"hidden"):-node(X),jay!=X.
attr(node,Y,class,@concat("click_",X,"_visible")):-related(X,Y).
attr(node,Y,class,@concat("mouseenter_",X,"_focus")):-related(X,Y).
attr(node,Y,class,@concat("mouseleave_",X,"_blur")):-related(X,Y).
attr(node,X,class,@concat("mouseenter_",X,"_focus")):-person(X).
attr(node,X,class,@concat("mouseleave_",X,"_blur")):-person(X).