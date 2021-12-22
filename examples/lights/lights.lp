
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Graph 1 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%% Graph %%%%%%%%%%%%%%

% Define the graph name
graph(house_1).

% Type and name as attributes
attr(graph,house_1,type,graph).
attr(graph,house_1,name,"Big House").

% Any type of atributes
attr(graph, house_1, nodesep,1).


%%%%%%%%%%%%%% Cluster/Subgraph %%%%%%%%%%%%%%

% Define clusters also as graphs contained in another different graph
graph(bedroom_1,house_1).
graph(livingroom_1,house_1).
graph(bathroom_1,livingroom_1).

% Define attributes for the clusters
attr(graph, bedroom_1, label, "Bedroom").
attr(graph, bedroom_1, style, dashed).

attr(graph, livingroom_1, label, "Livingroom").
attr(graph, livingroom_1, style, dashed).

attr(graph, bathroom_1, label, "Bathroom").
attr(graph, bathroom_1, style, "dotted").


%%%%%%%%%%%%%% Global Node/Edge attrubutes %%%%%%%%%%%%%%

% To reuse attributes for nodes and edges using a name

attr(graph_nodes,house_1,node,shape,record).
attr(graph_edges,house_1,style,dotted).


%%%%%%%%%%%%%% Nodes %%%%%%%%%%%%%%

% Define nodes assigned to a graph/subgraph
node(lhub_1,house_1).
node(lbathroom_1,bathroom_1).
node(lbedroom_1,bedroom_1).
node(llivingroom1_1,livingroom_1).
node(llivingroom2_1,livingroom_1).


is_light(lbathroom_1).
is_light(lbedroom_1).
is_light(llivingroom1_1).
is_light(llivingroom2_1).

attr(node,ID,shape,circle):-is_light(ID).
attr(node,ID,color,lightblue):-is_light(ID).
attr(node,ID,style,filled):-is_light(ID).

% Any other attributes
attr(node, lhub_1, label, "HUB").
attr(node, lbathroom_1, label, "Light").
attr(node, lbedroom_1, label, "Bed light").
attr(node, llivingroom1_1, label, "Main light").
attr(node, llivingroom2_1, label, "Kitchen light").


%%%%%%%%%%%%%% Edges %%%%%%%%%%%%%%

% Edges between nodes assigned to a graph
% No need to attach a cluster as the edges pass between clusters
edge((lhub_1,lbathroom_1), house_1).
edge((lhub_1,lbedroom_1), house_1).
edge((lhub_1,llivingroom1_1), house_1).
edge((lhub_1,llivingroom2_1), house_1).




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Graph 2 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%% Graph %%%%%%%%%%%%%%

% Define the graph name
graph(house_2).

% Type and name as attributes
attr(graph,house_2,type,graph).
attr(graph,house_2,name,"Single room House").

% Any type of atributes
attr(graph, house_2, nodesep,1).


%%%%%%%%%%%%%% Cluster/Subgraph %%%%%%%%%%%%%%

% Define clusters
graph(bedroom_2, house_2).
graph(bathroom_2, bedroom_2).

% Define attributes for the graphs
attr(graph, bedroom_2, label, "Bedroom").
attr(graph, bedroom_2, style, "dashed").

attr(graph, bathroom_2, label, "Bathroom").
attr(graph, bathroom_2, style, "dotted").

%%%%%%%%%%%%%% Global Node/Edge attrubutes %%%%%%%%%%%%%%

% To reuse attributes for nodes and edges using a name

attr(graph_nodes,house_2,node,shape,record).
attr(graph_edges,house_2,style,dotted).

%%%%%%%%%%%%%% Nodes %%%%%%%%%%%%%%

% Define nodes
node(lbathroom_2,bedroom_2).
node(lbedroom_2,bathroom_2).

is_light(lbathroom_2;lbedroom_2).

% Any other attributes
attr(node, lbathroom_2, label, "Light").
attr(node, lbedroom_2, label, "Main light").
