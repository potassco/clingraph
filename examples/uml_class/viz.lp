% Class names capitalized
uml_class_name(Class,@stringify(Class,true)):-uml_class(Class).


% Defaults
uml_class_name_i(Class,Class):- 
    uml_class(Class), 
    not uml_class_name(Class,_).
uml_class_name_i(Class,Name):- 
    uml_class_name(Class,Name).
uml_class_type_i(Class,concrete):- 
    uml_class(Class),
    not uml_class_type(Class,_).
uml_class_type_i(Class,Type):- 
    uml_class_type(Class,Type).
uml_attr_name_i(Class,Attr,Attr):- 
    uml_attr(Class,Attr), 
    not uml_attr_name(Class,Attr,_).
uml_attr_name_i(Class,Attr,Name):- 
    uml_attr_name(Class,Attr,Name).
uml_attr_visibility_i(Class,Attr,none):- 
    uml_attr(Class,Attr),
     not uml_attr_visibility(Class,Attr,_).
uml_attr_visibility_i(Class,Attr,Vis):- 
    uml_attr_visibility(Class,Attr,Vis).
uml_op_name_i(Class,Op,Op):- 
    uml_op(Class,Op), 
    not uml_op_name(Class,Op,_).
uml_op_name_i(Class,Op,Name):- 
    uml_op_name(Class,Op,Name).
uml_op_visibility_i(Class,Op,none):- 
    uml_op(Class,Op),
     not uml_op_visibility(Class,Op,_).
uml_op_visibility_i(Class,Op,Vis):- 
    uml_op_visibility(Class,Op,Vis).
uml_op_args_i(Class,Op,()):- 
    uml_op(Class,Op),
     not uml_op_args(Class,Op,_).
uml_op_args_i(Class,Op,Args):- 
    uml_op_args(Class,Op,Args).

visibility_symbol(protected,"#").
visibility_symbol(private,"-").
visibility_symbol(public,"+").
visibility_symbol(none,"").
%--------------- Graph

attr(graph_nodes, default, shape, rectangle).
attr(graph, default, splines, ortho).
attr(graph, default, nodesep, "3").
attr(graph, default, rankdir, "TB").
attr(graph, default, fontsize, 20).

%--------------- Nodes

% Classes as Nodes
node(Name) :- uml_class(Name).

attr(node,Class,label,@concat("<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0' CELLPADDING='1'>",
                        "<TR><TD ><B>{{name}} </B></TD></TR>",
                        "<TR><TD ALIGN='left'> {% if attr is string %}{{ attr }} {% else %} {% for a in attr %} {{a}} {% endfor %} {% endif %}</TD></TR>",
                        "<TR><TD ALIGN='left'> {% if op is string %}{{ op }} {% else %} {% for a in op %} {{a}} {% endfor %} {% endif %}</TD></TR>",
                        "</TABLE>>")):-
    uml_class(Class).

attr(node,Class,(label,name),Name):-
    uml_class_name_i(Class,Name).

attr(node,Class,(label,attr),@f("{2}{0}: {1}<br ALIGN='left' />",Name,Type,V)):-
    uml_attr(Class,Attr),
    uml_attr_name_i(Class,Attr,Name),
    uml_attr_type(Class,Attr,Type),
    uml_attr_visibility_i(Class,Attr,Visibility),
    visibility_symbol(Visibility, V).

attr(node,Class,(label,op),@op_str(Name,Type,V,Args)):-
    uml_op(Class,Op),
    uml_op_name_i(Class,Op,Name),
    uml_op_type(Class,Op,Type),
    uml_op_visibility_i(Class,Op,Visibility),
    uml_op_args_i(Class,Op,Args),
    visibility_symbol(Visibility, V).


attr(node, T, style, "filled"):- node(T).
attr(node, T, fillcolor, "#FFFFCE"):- node(T).
attr(node, T, color, "black"):- node(T).
attr(node, T, margin, 0):- node(T).
attr(node, T, width, 0):- node(T).
attr(node, T, hight, 0):- node(T).


%--------------- Edges


%%%% Is a

edge((SuperClass,SubClass)):-uml_is_a(SubClass,SuperClass).
attr(edge,(SuperClass,SubClass),dir,back):-uml_is_a(SubClass,SuperClass).
attr(edge,(SuperClass,SubClass),arrowtail,empty):-uml_is_a(SubClass,SuperClass).


%%%% Associations (agregation, composition, uni, bi)

edge((Class1,Class2,Assoc)):-uml_assoc(Class1,Class2,Assoc).
attr(edge,(Class1,Class2,Assoc),dir,both):-
    uml_assoc(Class1,Class2,Assoc).
attr(edge,ID,arrowsize,"0.8"):-
    edge(ID).
% Agregation
attr(edge,(Class1,Class2,Assoc),arrowhead,odiamond):-
    uml_assoc_type(Class1,Class2,Assoc,agregation).
attr(edge,(Class1,Class2,Assoc),arrowtail,open):-
    uml_assoc_type(Class1,Class2,Assoc,agregation).
% Composition
attr(edge,(Class1,Class2,Assoc),arrowhead,diamond):-
    uml_assoc_type(Class1,Class2,Assoc,composition).
attr(edge,(Class1,Class2,Assoc),arrowtail,open):-
    uml_assoc_type(Class1,Class2,Assoc,composition).
% Uni-directional
attr(edge,(Class1,Class2,Assoc),arrowhead,none):-
    uml_assoc_type(Class1,Class2,Assoc,uni).
attr(edge,(Class1,Class2,Assoc),arrowtail,open):-
    uml_assoc_type(Class1,Class2,Assoc,uni).
% Bi-directional
attr(edge,(Class1,Class2,Assoc),arrowhead,none):-
    uml_assoc_type(Class1,Class2,Assoc,bi).
attr(edge,(Class1,Class2,Assoc),arrowtail,none):-
    uml_assoc_type(Class1,Class2,Assoc,bi).




% Labels

% Label for the association
attr(edge,(Class1,Class2,Assoc),xlabel,Name):-
    uml_assoc_name(Class1,Class2,Assoc,Name).

% Label for the multiplicity
edge_property(headlabel).
edge_property(taillabel).

attr(edge,(Class1,Class2,Assoc), P, @concat("<<TABLE BORDER='0'>",
                                                "<TR><TD><FONT POINT-SIZE='11'>{{name}}</FONT></TD></TR>",
                                                "<TR><TD><FONT POINT-SIZE='8' COLOR='gray40'>{{min}}{{sep}}{{max}}</FONT></TD></TR>",
                                         "</TABLE>>")):-
    uml_assoc(Class1,Class2,Assoc),
    edge_property(P).

assoc_label((Class1,Class2,Assoc),Class3,min,Min) :- 
    uml_assoc_cadinality(Class1,Class2,Assoc,Class3,Min,Max).
assoc_label((Class1,Class2,Assoc),Class3,sep,"...") :- 
    uml_assoc_cadinality(Class1,Class2,Assoc,Class3,Min,Max), Min!=Max.
assoc_label((Class1,Class2,Assoc),Class3,sep,"") :- 
    uml_assoc_cadinality(Class1,Class2,Assoc,Class3,Min,Min).
assoc_label((Class1,Class2,Assoc),Class3,max,Max) :- 
    uml_assoc_cadinality(Class1,Class2,Assoc,Class3,Min,Max),Min!=Max.
assoc_label((Class1,Class2,Assoc),Class3,max,"") :- 
    uml_assoc_cadinality(Class1,Class2,Assoc,Class3,Max,Max).
assoc_label((Class1,Class2,Assoc),Class3,name,Name) :- 
    uml_assoc_name(Class1,Class2,Assoc,Class3,Name).

attr(edge,(Class1,Class2,Assoc),(taillabel,Name),Value) :- assoc_label((Class1,Class2,Assoc),Class1,Name,Value).
attr(edge,(Class1,Class2,Assoc),(headlabel,Name),Value) :- assoc_label((Class1,Class2,Assoc),Class2,Name,Value).




#script (python)
from clingo.symbol import String

def op_str(name,op_type,visibility,args):
    name = str(name).strip('"')
    op_type = str(op_type).strip('"')
    visibility = str(visibility).strip('"')
    args_processed = []
    for a in args.arguments:
        n = str(a.arguments[0])
        t = str(a.arguments[1])
        args_processed.append(f"{n}:{t}")
    args_str = ",".join(args_processed)
    s = f"{visibility} {name}({args_str}) : {op_type}<br ALIGN='left' /> "
    return String(s)

#end.