% Instance
start(a). end(g).
city(a). city(b). city(c). city(d). 
city(e). city(f). city(g).
road(a,b,3). road(a,c,4).
road(b,c,1). road(b,d,1).
road(c,d,2). road(c,e,6).
road(d,e,4). road(d,f,7).
road(e,f,3). road(e,g,2).
road(f,g,5).

% Encoding
{in_path(X,Y)}:-road(X,Y,_).
connected(X,Y):-in_path(X,Y).
connected(X,Z):-connected(X,Y), in_path(Y,Z).
:- not connected(X,Y), start(X), end(Y).
#minimize{S,(X,Y):in_path(X,Y),road(X,Y,S)}.
