
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Graph 1 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%% Graph %%%%%%%%%%%%%%

% Define the graph name
graph(house_1).

% Type and name as attributes
attr(graph,house_1,type,digraph).
attr(graph,house_1,name,"Big House").

% Any type of atributes
attr(graph, house_1, nodesep,1).


%%%%%%%%%%%%%% Cluster/Subgraph %%%%%%%%%%%%%%

% Define clusters
cluster(bedroom_1).
cluster(livingroom_1).
cluster(bathroom_1).

% Attach cluster to specific graph
% If ommited 'default' graph will be used
attr(cluster, bedroom_1_1, graph, house_1).
attr(cluster, livingroom_1, graph, house_1).
attr(cluster, bathroom_1, graph, house_1).

% Define attributes for the clusters
attr(cluster, livingroom_1, label, "Bedroom").
attr(cluster, livingroom_1, style, dashed).

attr(cluster, livingroom_1, label, "Livingroom").
attr(cluster, livingroom_1, style, dashed).

attr(cluster, bathroom_1, label, "Bathroom").
attr(cluster, bathroom_1, style, "dotted").

% A cluster inside a cluster
attr(cluster, bathroom_1, cluster, livingroom_1).


%%%%%%%%%%%%%% Classes %%%%%%%%%%%%%%

% To reuse attributes for nodes and edges using a name

% 'node' and 'edge' apply to all node and edges of all graphs
attr(class,node,shape,record).
attr(class,edge,style,dotted).

%  other names can also be defined and they will be available in all graphs
attr(class,light,color,lightblue).
attr(class,light,style,filled).


%%%%%%%%%%%%%% Nodes %%%%%%%%%%%%%%

% Define nodes
node(lhub_1).
node(lbathroom_1).
node(lbedroom_1).
node(llivingroom1_1).
node(llivingroom2_1).

% Attach to a graph, or 'default' will be used
attr(node, lhub_1, graph, house_1).
attr(node, lbathroom_1, graph, house_1).
attr(node, lbedroom_1, graph, house_1).
attr(node, llivingroom1_1, graph, house_1).
attr(node, llivingroom2_1, graph, house_1).

% Attach to a cluster, or it will be part of the main graph
attr(node, lbathroom_1, cluster, bathroom_1).
attr(node, lbedroom_1, cluster, bedroom_1).
attr(node, llivingroom1_1, cluster, livingroom_1).
attr(node, llivingroom2_1, cluster, livingroom_1).


% Use special attribute class to use the class previously defined
attr(node, lbathroom_1, class, light).
attr(node, lbedroom_1, class, light).
attr(node, llivingroom1_1, class, light).
attr(node, llivingroom2_1, class, light).

% Any other attributes
attr(node, lbathroom_1, label, "Light").
attr(node, lbedroom_1, label, "Bed light").
attr(node, llivingroom1_1, label, "Main light").
attr(node, llivingroom2_1, label, "Kitchen light").


%%%%%%%%%%%%%% Edges %%%%%%%%%%%%%%

% Edges between nodes
graphviz_edge((lhub_1,lbathroom_1)).
graphviz_edge((lhub_1,lbedroom_1)).
graphviz_edge((lhub_1,llivingroom1_1)).
graphviz_edge((lhub_1,llivingroom2_1)).

% Attach to a graph, or 'default' will be used
attr(edge, (lhub_1,lbathroom_1), graph, house_1).
attr(edge, (lhub_1,lbedroom_1), graph, house_1).
attr(edge, lbedroom_1, graph, house_1).
attr(edge, (lhub_1,llivingroom1_1), graph, house_1).
attr(edge, (lhub_1,llivingroom2_1), graph, house_1)

% No need to attach a cluster as the edges pass between clusters



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Graph 2 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%% Graph %%%%%%%%%%%%%%

% Define the graph name
graph(house_2).

% Type and name as attributes
attr(graph,house_2,type,digraph).
attr(graph,house_2,name,"Single room House").

% Any type of atributes
attr(graph, house_2, nodesep,1).


%%%%%%%%%%%%%% Cluster/Subgraph %%%%%%%%%%%%%%

% Define clusters
cluster(bedroom_2).
cluster(bathroom_2).

% Attach cluster to specific graph
% If ommited 'default' graph will be used
attr(cluster, bedroom_2_2, graph, house_2).
attr(cluster, bathroom_2, graph, house_2).

% Define attributes for the clusters


attr(cluster, bathroom_2, label, "Bathroom").
attr(cluster, bathroom_2, style, "dotted").

% A cluster inside a cluster


%%%%%%%%%%%%%% Classes %%%%%%%%%%%%%%

% To reuse attributes for nodes and edges using a name

% 'node' and 'edge' apply to all node and edges of all graphs
attr(class,node,shape,record).
attr(class,edge,style,dotted).

%  other names can also be defined and they will be available in all graphs
attr(class,light,color,lightblue).
attr(class,light,style,filled).


%%%%%%%%%%%%%% Nodes %%%%%%%%%%%%%%

% Define nodes
node(lbathroom_2).
node(lbedroom_2).

% Attach to a graph, or 'default' will be used
attr(node, lhub_2, graph, house_2).
attr(node, lbathroom_2, graph, house_2).
attr(node, lbedroom_2, graph, house_2).

% Attach to a cluster, or it will be part of the main graph
attr(node, lbathroom_2, cluster, bathroom_2).
attr(node, lbedroom_2, cluster, bedroom_2).


% Use special attribute class to use the class previously defined
attr(node, lbathroom_2, class, light).
attr(node, lbedroom_2, class, light).

% Any other attributes
attr(node, lbathroom_2, label, "Light").
attr(node, lbedroom_2, label, "Main light").

