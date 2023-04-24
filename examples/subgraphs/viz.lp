graph(house).
attr(graph,house,nodesep,2).%Horizontal separation
attr(graph,house,ranksep,2).%Vertical separation
graph(R,house):-room(R).
attr(graph,R,label,@stringify(R,true)):-room(R).
node(X,R):-thing(X,R).
link((X1,R1),(X2,R2)):- door(R1,R2), thing(X1,R1), thing(X2,R2),
    #false: thing(X1',R1), X1>X1' ; #false: thing(X2',R2), X2>X2'.
    % Linking only one thing on the room to another thing in the adjecent room
edge((X1,X2),house):-link((X1,R1),(X2,R2)).
attr(graph,house,compound,true). % <---- Needed for ltail to work
attr(edge,(X1,X2),ltail,@cluster(R1)):-link((X1,R1),(X2,R2)) .
attr(edge,(X1,X2),lhead,@cluster(R2)):-link((X1,R1),(X2,R2)).