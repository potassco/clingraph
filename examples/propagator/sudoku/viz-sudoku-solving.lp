graph(I):- _step_type(_,I).
attr(graph,I,margin,"0,0"):- _step_type(T,I).
% attr(graph,I,fontsize,40):- _step_type(T,I).
% attr(graph,I,(label,0),@concat("(",I,") ")):- _step_type(T,I).
% attr(graph,I,(label,1),T):- _step_type(T,I).

% Global graph attributes
attr(graph, I, nodesep, 1):-graph(I).
attr(graph, I, newrank, true):-graph(I).

% Global node attributes
attr(graph_nodes, I, shape, square):-graph(I).
attr(graph_nodes, I, style, filled):-graph(I).

attr(graph_nodes, I, fillcolor, white):-graph(I).
attr(graph_nodes, I, width, "1"):-graph(I).
attr(graph_nodes, I, fixedsize, "true"):-graph(I).

#const green= "#05BE1C".
#const yellow= "#EEDC07".
#const red= "#F90B0B".
#const size = 3.
value(1..size*size).

table_pos(X,X+((X-1)/size)+1):-_true(pos(X,_)).

node(pos(X,Y), I):- _true(pos(X,Y)), graph(I).
attr(node, pos(X,Y), fillcolor, "grey88"):- _true(pos(X,Y)), graph(I),  _true(subgrid(X,Y,S)), S\2==0.

attr(node, pos(X,Y), pos, @pos(X,Y)):- _true(pos(X,Y)).
attr(node, pos(X,Y), label, V ):- _true(initial(X,Y,V)).
attr(node, pos(X,Y), fontsize,40 ):- _true(initial(X,Y,V)).

attr(node, pos(X,Y), (label,0), "<<table BORDER='0'>"):- _true(pos(X,Y)), not  _true(initial(X,Y,_)).
attr(node, pos(X,Y), (label,1), "<tr>"):- _true(pos(X,Y)), not  _true(initial(X,Y,_)).
attr(node, pos(X,Y), (label,5), "</tr><tr>"):- _true(pos(X,Y)), not  _true(initial(X,Y,_)), _undefined(sudoku(X,Y,_)).
attr(node, pos(X,Y), (label,9), "</tr><tr>"):- _true(pos(X,Y)), not  _true(initial(X,Y,_)), _undefined(sudoku(X,Y,_)).
attr(node, pos(X,Y), (label,13), "</tr></table>>"):- _true(pos(X,Y)), not  _true(initial(X,Y,_)).

opacity(sudoku(X,Y,V),99):-_change(sudoku(X,Y,V)).
opacity(sudoku(X,Y,V),35):-not _change(sudoku(X,Y,V)), _true(pos(X,Y)), value(V).
border(sudoku(X,Y,V),1):-_change(sudoku(X,Y,V)).
border(sudoku(X,Y,V),0):-not _change(sudoku(X,Y,V)), _true(pos(X,Y)), value(V).

attr(node, pos(X,Y), fontsize, 20) :- _true(sudoku(X,Y,V)), not _true(initial(X,Y,_)).

attr(node,pos(X,Y),(label,3),L) :- _true(sudoku(X,Y,V)), not _true(initial(X,Y,_)),%%#(\label{lst:vizsudoku:proptrue:start}#)
  opacity(sudoku(X,Y,V),O), border(sudoku(X,Y,V),B),%%#(\label{lst:vizsudoku:proptrue:opacbord}#)
  L=@concat("<td BGCOLOR='",green,O,"' BORDER='",B,"'>",V,"</td>").%%#(\label{lst:vizsudoku:proptrue:end}#)

attr(node,pos(X,Y),(label,P),L) :- _undefined(sudoku(X,Y,V)), not _decide(sudoku(X,Y,V),_),%%#(\label{lst:vizsudoku:undef:start}#) 
  opacity(sudoku(X,Y,V),O), border(sudoku(X,Y,V),B), table_pos(V,P), 
  L=@concat("<td BGCOLOR='",yellow,O,"' BORDER='",B,"'>",V,"</td>").%%#(\label{lst:vizsudoku:undef:end}#) 

attr(node, pos(X,Y), (label,P), L):- _false(sudoku(X,Y,V)), _undefined(sudoku(X,Y,_)), 
  table_pos(V,P), not  _true(initial(X,Y,_)), opacity(sudoku(X,Y,V),O), border(sudoku(X,Y,V),B),
  L=@concat("<td BORDER='",B,"'>","&nbsp;","</td>").

attr(node,pos(X,Y),(label,P),L) :- _decide(sudoku(X,Y,V),neg), table_pos(V,P),%%#(\label{lst:vizsudoku:decide:start}#) 
  L=@concat("<td BGCOLOR='",red,"99' BORDER='1'><B>",V,"</B></td>").%%#(\label{lst:vizsudoku:decide:end}#)  

attr(node, pos(X,Y), (label,P), @concat("<td BGCOLOR='#509F5D99' BORDER='1'><B>",V,"</B></td>")):- _decide(sudoku(X,Y,V),pos), table_pos(V,P).
