graph(T):-time(T).
node((X,T),T):-floor(X),time(T).
attr(graph,T,(label,1),T):-time(T).
attr(graph,T,(label,0),"Time:"):-time(T).
attr(graph,T,bgcolor,"white"):-time(T).
attr(node,(X,T),shape,none):-floor(X),time(T), not at(X,T).
attr(node,(X,T),shape,square):-floor(X),time(T),at(X,T).
attr(node,(X,T),width,"0.5"):-floor(X),time(T).
attr(node,(X,T),hight,"0.5"):-floor(X),time(T).
attr(node,(X,T),label,X):-floor(X),time(T).
attr(node,(X,T),(pos,0),0):-floor(X),time(T).
attr(node,(X,T),(pos,1),X+1):-floor(X),time(T).
attr(node,(X,T),(pos,"sep"),","):-floor(X),time(T).
attr(node,(X,T),fontcolor,red):-floor(X),time(T),called(X,T).
attr(node,(X,T),color,green):-floor(X),time(T),served(X,T).
edge(((X,T),(X+1,T)),T):-floor(X),floor(X+1),time(T).

