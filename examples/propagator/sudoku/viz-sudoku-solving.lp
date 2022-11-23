#defined _decide/2.
#defined _change/1.
#defined _true/1.
#defined _undefined/1.

#const green= "#05BE1C".
% #const yellow= "#EEDC07".
#const red= "#F90B0B".
#const white= "#FFFFFF".
#const size = 3.
value(1..size*size).


graph(I):- _step_type(_,I).
attr(graph,I,margin,"0,0"):- _step_type(T,I).
attr(graph, I, nodesep, 1):-graph(I).
attr(graph, I, newrank, true):-graph(I).

% Graph label 
% attr(graph,I,fontsize,40):- _step_type(T,I).
% attr(graph,I,(label,0),@concat("(",I,") ")):- _step_type(T,I).
% attr(graph,I,(label,1),T):- _step_type(T,I).

% Global node attributes
attr(graph_nodes, I, shape, square):-graph(I).
attr(graph_nodes, I, style, filled):-graph(I).
attr(graph_nodes, I, fillcolor, white):-graph(I).
attr(graph_nodes, I, width, "1"):-graph(I).
attr(graph_nodes, I, fixedsize, "true"):-graph(I).

node(pos(X,Y), I):- _true(pos(X,Y)), graph(I).
attr(node, pos(X,Y), fillcolor, "grey88"):- _true(pos(X,Y)), graph(I),  _true(subgrid(X,Y,S)), S\2==0.
attr(node, pos(X,Y), pos, @pos(X,Y)):- _true(pos(X,Y)).

% --- Label templates

% Initial values
attr(node, pos(X,Y), fontsize,40 ):- _true(initial(X,Y,V)).
attr(node, pos(X,Y), label, V ):- _true(initial(X,Y,V)).

% Values defined as true
attr(node, pos(X,Y), fontsize, 20) :- _true(sudoku(X,Y,V)), not _true(initial(X,Y,_)).
attr(node, pos(X,Y), label, @concat("<<table BORDER='0'>",
                                "<tr><td BGCOLOR='{{",color,"[",V,"]}}{{",opacity,"[",V,"]}}'",
                                       " BORDER='{{",border,"[",V,"]}}'>",
                                      "{{",value,"[",V,"]}}",
                                "</td></tr></table>>")):-
  _true(sudoku(X,Y,V)), not  _true(initial(X,Y,_)). 

% Cells with multiple options
attr(node, pos(X,Y), label, @concat("<<table BORDER='0'>",
                              "<tr>",
                                "<td BGCOLOR='{{color[1]}}{{opacity[1]}}' BORDER='{{border[1]}}'>{{value[1]}}</td>",
                                "<td BGCOLOR='{{color[2]}}{{opacity[2]}}' BORDER='{{border[2]}}'>{{value[2]}}</td>",
                                "<td BGCOLOR='{{color[3]}}{{opacity[3]}}' BORDER='{{border[3]}}'>{{value[3]}}</td>",
                              "</tr>",
                              "<tr>",
                                "<td BGCOLOR='{{color[4]}}{{opacity[4]}}' BORDER='{{border[4]}}'>{{value[4]}}</td>",
                                "<td BGCOLOR='{{color[5]}}{{opacity[5]}}' BORDER='{{border[5]}}'>{{value[5]}}</td>",
                                "<td BGCOLOR='{{color[6]}}{{opacity[6]}}' BORDER='{{border[6]}}'>{{value[6]}}</td>",
                              "</tr>",
                              "<tr>",
                                "<td BGCOLOR='{{color[7]}}{{opacity[7]}}' BORDER='{{border[7]}}'>{{value[7]}}</td>",
                                "<td BGCOLOR='{{color[8]}}{{opacity[8]}}' BORDER='{{border[8]}}'>{{value[8]}}</td>",
                                "<td BGCOLOR='{{color[9]}}{{opacity[9]}}' BORDER='{{border[9]}}'>{{value[9]}}</td>",
                              "</tr>",
                              "</table>>")):- 
  _true(pos(X,Y)), not  _true(initial(X,Y,_)), not _true(sudoku(X,Y,_)).

% --- Label values for replacement 

% Changes shown with opacity
attr(node, pos(X,Y), (label,opacity,V), 25):- not _change(sudoku(X,Y,V)), not _decide(sudoku(X,Y,V),_), _true(sudoku(X,Y,V)).
attr(node, pos(X,Y), (label,opacity,V), "00"):- not _true(sudoku(X,Y,V)), not _decide(sudoku(X,Y,V),neg), _true(pos(X,Y)), value(V).

% Decisions shown with border
attr(node, pos(X,Y), (label,border,V), 1):-_decide(sudoku(X,Y,V),_).
attr(node, pos(X,Y), (label,border,V), 0):-not _decide(sudoku(X,Y,V),_), _true(pos(X,Y)), value(V).

% State shown with color
attr(node, pos(X,Y), (label,color,V), white):-not _true(sudoku(X,Y,V)), not _decide(sudoku(X,Y,V),_), _true(pos(X,Y)), value(V).
attr(node, pos(X,Y), (label,color,V), green):-_true(sudoku(X,Y,V)).
attr(node, pos(X,Y), (label,color,V), red):-_decide(sudoku(X,Y,V),neg).
attr(node, pos(X,Y), (label,color,V), green):-_decide(sudoku(X,Y,V),pos).

% Value for everything but _false
attr(node, pos(X,Y), (label,value,V), V):-_true(sudoku(X,Y,V)).
attr(node, pos(X,Y), (label,value,V), V):-_undefined(sudoku(X,Y,V)).
attr(node, pos(X,Y), (label,value,V), ""):-_false(sudoku(X,Y,V)).