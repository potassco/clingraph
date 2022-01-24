
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



attr(node,lbathroom_1,shape,circle).
attr(node,lbathroom_1,color,lightblue).
attr(node,lbathroom_1,style,filled).

attr(node,lbedroom_1,shape,circle).
attr(node,lbedroom_1,color,lightblue).
attr(node,lbedroom_1,style,filled).

attr(node,llivingroom1_1,shape,circle).
attr(node,llivingroom1_1,color,lightblue).
attr(node,llivingroom1_1,style,filled).

attr(node,llivingroom2_1,shape,circle).
attr(node,llivingroom2_1,color,lightblue).
attr(node,llivingroom2_1,style,filled).

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

attr(node,lbathroom_2,shape,circle).
attr(node,lbathroom_2,color,lightblue).
attr(node,lbathroom_2,style,filled).

attr(node,lbedroom_2,shape,circle).
attr(node,lbedroom_2,color,lightblue).
attr(node,lbedroom_2,style,filled).


% Any other attributes
attr(node, lbathroom_2, label, "Light").
attr(node, lbedroom_2, label, "Main light").
