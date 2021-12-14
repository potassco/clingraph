% #show.
% #show init/2.



% #show occurs(object(robot,R), action(move,   D      ), T) :    move(robot(R),D,T).
% #show occurs(object(robot,R), action(pickup, ()     ), T) :  pickup(robot(R),_,T).
% #show occurs(object(robot,R), action(putdown,()     ), T) : putdown(robot(R),_,T).

% #show occurs(object(robot,R), action(deliver,(O,A  )), T) : process(product(A),order(O),C,T), toShelf(S,C), position(robot(R),C,T-1).
% #show occurs(object(robot,R), action(deliver,(O,A  )), T) : process(product(A),order(O),C,T), atShelf(S,C,T-1), carries(robot(R),S,T-1).
% #show occurs(object(robot,R), action(deliver,(O,A  )), T) : process(product(A),order(O),C,T), position(S,C,T), carries(robot(R),S,T-1), shelved(S,product(A)).
% #show occurs(object(robot,R), action(deliver,(O,A,N)), T) : process(product(A),order(O),S,N,T), carries(robot(R),S,T-1).
