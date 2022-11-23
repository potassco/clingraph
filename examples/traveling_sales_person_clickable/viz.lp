#show node(X):city(X,_).
#show edge((X,Y)):connection(X,Y,T),cycle(X,Y,T).
#show attr(node,X,"URL",URL):city(X,URL).
#show attr(node,X,style,filled):start(X).
#show attr(node,X,color,blue):start(X).
#show attr(edge,(X,Y),label,@format("{} {}h",T,C)):time(X,Y,T,C),cycle(X,Y,T).
#show attr(edge,(X,Y),color,blue):cycle(X,Y,T).
#show attr(edge,(X,Y),textcolor,blue):cycle(X,Y,T).