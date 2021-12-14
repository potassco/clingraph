%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% = Command-line Arguments =================================
% -x 5 -y 5 -s 1 -p 1 -r 1 -P 1 -u 1 -o 1 -H
%
% = Instance Statistics ====================================
% Grid Size X:                      5
% Grid Size Y:                      5
% Number of Nodes:                  25
% Number of Highway Nodes:          21
% Number of Robots:                 1
% Number of Shelves:                1
% Number of Picking Stations:       1
% Number of Products:               1
% Number of Product Units in Total: 1
% Number of Orders:                 1
% Number of Orders Lines:           1
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#program base.

% init
init(object(highway,1),value(at,(1,1))).
init(object(highway,2),value(at,(2,1))).
init(object(highway,4),value(at,(4,1))).
init(object(highway,5),value(at,(5,1))).
init(object(highway,6),value(at,(1,2))).
init(object(highway,7),value(at,(2,2))).
init(object(highway,8),value(at,(3,2))).
init(object(highway,9),value(at,(4,2))).
init(object(highway,10),value(at,(5,2))).
init(object(highway,11),value(at,(1,3))).
init(object(highway,14),value(at,(4,3))).
init(object(highway,15),value(at,(5,3))).
init(object(highway,16),value(at,(1,4))).
init(object(highway,17),value(at,(2,4))).
init(object(highway,18),value(at,(3,4))).
init(object(highway,19),value(at,(4,4))).
init(object(highway,20),value(at,(5,4))).
init(object(highway,22),value(at,(2,5))).
init(object(highway,23),value(at,(3,5))).
init(object(highway,24),value(at,(4,5))).
init(object(highway,25),value(at,(5,5))).
init(object(node,1),value(at,(1,1))).
init(object(node,2),value(at,(2,1))).
init(object(node,3),value(at,(3,1))).
init(object(node,4),value(at,(4,1))).
init(object(node,5),value(at,(5,1))).
init(object(node,6),value(at,(1,2))).
init(object(node,7),value(at,(2,2))).
init(object(node,8),value(at,(3,2))).
init(object(node,9),value(at,(4,2))).
init(object(node,10),value(at,(5,2))).
init(object(node,11),value(at,(1,3))).
init(object(node,12),value(at,(2,3))).
init(object(node,13),value(at,(3,3))).
init(object(node,14),value(at,(4,3))).
init(object(node,15),value(at,(5,3))).
init(object(node,16),value(at,(1,4))).
init(object(node,17),value(at,(2,4))).
init(object(node,18),value(at,(3,4))).
init(object(node,19),value(at,(4,4))).
init(object(node,20),value(at,(5,4))).
init(object(node,21),value(at,(1,5))).
init(object(node,22),value(at,(2,5))).
init(object(node,23),value(at,(3,5))).
init(object(node,24),value(at,(4,5))).
init(object(node,25),value(at,(5,5))).
init(object(order,1),value(line,(1,1))).
init(object(order,1),value(pickingStation,1)).
init(object(pickingStation,1),value(at,(3,1))).
init(object(product,1),value(on,(1,1))).
init(object(robot,1),value(at,(1,5))).
init(object(shelf,1),value(at,(3,3))).
