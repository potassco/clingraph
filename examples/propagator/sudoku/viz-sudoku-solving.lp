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
                                "<tr><td BGCOLOR='{{",@concat(color,V),"}}{{",@concat(opacity,V),"}}'",
                                       " BORDER='{{",@concat(border,V),"}}'>",
                                      "{{",@concat(value,V),"}}",
                                "</td></tr></table>>")):-
  _true(sudoku(X,Y,V)), not  _true(initial(X,Y,_)). 

% Cells with multiple options
attr(node, pos(X,Y), label, @concat("<<table BORDER='0'>",
                              "<tr>",
                                "<td BGCOLOR='{{color1}}{{opacity1}}' BORDER='{{border1}}'>{{value1}}</td>",
                                "<td BGCOLOR='{{color2}}{{opacity2}}' BORDER='{{border2}}'>{{value2}}</td>",
                                "<td BGCOLOR='{{color3}}{{opacity3}}' BORDER='{{border3}}'>{{value3}}</td>",
                              "</tr>",
                              "<tr>",
                                "<td BGCOLOR='{{color4}}{{opacity4}}' BORDER='{{border4}}'>{{value4}}</td>",
                                "<td BGCOLOR='{{color5}}{{opacity5}}' BORDER='{{border5}}'>{{value5}}</td>",
                                "<td BGCOLOR='{{color6}}{{opacity6}}' BORDER='{{border6}}'>{{value6}}</td>",
                              "</tr>",
                              "<tr>",
                                "<td BGCOLOR='{{color7}}{{opacity7}}' BORDER='{{border7}}'>{{value7}}</td>",
                                "<td BGCOLOR='{{color8}}{{opacity8}}' BORDER='{{border8}}'>{{value8}}</td>",
                                "<td BGCOLOR='{{color9}}{{opacity9}}' BORDER='{{border9}}'>{{value9}}</td>",
                              "</tr>",
                              "</table>>")):- 
  _true(pos(X,Y)), not  _true(initial(X,Y,_)), not _true(sudoku(X,Y,_)).

% --- Label values for replacement 

% Changes shown with opacity
attr(node, pos(X,Y), (label,@concat(opacity,V)), 25):- not _change(sudoku(X,Y,V)), not _decide(sudoku(X,Y,V),_), _true(sudoku(X,Y,V)).
attr(node, pos(X,Y), (label,@concat(opacity,V)), "00"):- not _true(sudoku(X,Y,V)), not _decide(sudoku(X,Y,V),neg), _true(pos(X,Y)), value(V).

% Decisions shown with border
attr(node, pos(X,Y), (label,@concat(border,V)), 1):-_decide(sudoku(X,Y,V),_).
attr(node, pos(X,Y), (label,@concat(border,V)), 0):-not _decide(sudoku(X,Y,V),_), _true(pos(X,Y)), value(V).

% State shown with color
attr(node, pos(X,Y), (label,@concat(color,V)), white):-not _true(sudoku(X,Y,V)), not _decide(sudoku(X,Y,V),_), _true(pos(X,Y)), value(V).
attr(node, pos(X,Y), (label,@concat(color,V)), green):-_true(sudoku(X,Y,V)).
attr(node, pos(X,Y), (label,@concat(color,V)), red):-_decide(sudoku(X,Y,V),neg).
attr(node, pos(X,Y), (label,@concat(color,V)), green):-_decide(sudoku(X,Y,V),pos).

% Value for everything but _false
attr(node, pos(X,Y), (label,@concat(value,V)), V):-_true(sudoku(X,Y,V)).
attr(node, pos(X,Y), (label,@concat(value,V)), V):-_undefined(sudoku(X,Y,V)).
attr(node, pos(X,Y), (label,@concat(value,V)), ""):-_false(sudoku(X,Y,V)).