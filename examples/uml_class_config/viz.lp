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

%--------------- Graph

attr(graph_nodes, default, shape, rectangle).
attr(graph, default, splines, ortho).
attr(graph, default, nodesep, "3").
attr(graph, default, rankdir, "TB").
attr(graph, default, fontsize, 20).

%--------------- Nodes

% Classes as Nodes
node(Name) :- uml_class(Name).

attr(node,Class,(label,0),@record_label(Name,Type)):-
    uml_class(Class), 
    uml_class_name_i(Class,Name), 
    uml_class_type_i(Class,Type).
attr(node,Class,(label,4),@record_end()):-
    uml_class(Class).
attr(node,Class,(label,2),@new_row()):-
    uml_class(Class).
attr(node,Class,(label,1),@attr_str(Name,Type,Visibility)):-
    uml_attr(Class,Attr),
    uml_attr_name_i(Class,Attr,Name),
    uml_attr_type(Class,Attr,Type),
    uml_attr_visibility_i(Class,Attr,Visibility).
attr(node,Class,(label,3),@op_str(Name,Type,Visibility,Args)):-
    uml_op(Class,Op),
    uml_op_name_i(Class,Op,Name),
    uml_op_type(Class,Op,Type),
    uml_op_visibility_i(Class,Op,Visibility),
    uml_op_args_i(Class,Op,Args).


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
attr(edge,(Class1,Class2,Assoc),xlabel,Name):-
    uml_assoc_name(Class1,Class2,Assoc,Name).

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

assoc_label((Class1,Class2,Assoc),taillabel,X,Y) :- assoc_label((Class1,Class2,Assoc),Class1,X,Y).
assoc_label((Class1,Class2,Assoc),headlabel,X,Y) :- assoc_label((Class1,Class2,Assoc),Class2,X,Y).

edge_property(headlabel).
edge_property(taillabel).
attr(edge,(Class1,Class2,Assoc), (Property,0), "<<TABLE BORDER='0'><TR><TD><FONT POINT-SIZE='11'>"):-
    uml_assoc(Class1,Class2,Assoc),
    edge_property(Property).

attr(edge,(Class1,Class2,Assoc), (Property,2), "</FONT></TD></TR><TR><TD><FONT POINT-SIZE='8' COLOR='gray40'>"):-
    uml_assoc(Class1,Class2,Assoc),
    edge_property(Property).

attr(edge,(Class1,Class2,Assoc), (Property,6), "</FONT></TD></TR></TABLE>>"):-
    uml_assoc(Class1,Class2,Assoc),
    edge_property(Property).

pos(min,3). pos(sep,4). pos(max,5). pos(name,1).
attr(edge,ID, (Property,N), V):-
    assoc_label(ID,Property,O,V), pos(O,N).



#script (python)
from clingo.symbol import String
visibility_symbols={'protected':'#', 'public':'+','private':'-','none':' '}

def attr_str(name,attr_type,visibility):
    name = str(name).strip('"')
    attr_type = str(attr_type).strip('"')
    visibility = str(visibility).strip('"')
    if not visibility in visibility_symbols:
        raise RuntimeError(f'Invalid visibility: {visibility}')
    s = f"{visibility_symbols[visibility]} {name} : {attr_type}<br ALIGN='left' /> "
    return String(s)

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
    if not visibility in visibility_symbols:
        raise RuntimeError(f'Invalid visibility: {visibility}')
    s = f"{visibility_symbols[visibility]} {name}({args_str}) : {op_type}<br ALIGN='left' /> "
    return String(s)

def record_label(name,record_type):
    str_name = str(name).strip('"')
    str_type = str(record_type)
    if str_type =="abstract":
        t= ("<I>","</I>")
    else:
        t = ("","")
    
    s = f"<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0' CELLPADDING='1'><TR><TD ><B>{t[0]}{str_name}{t[1]}</B></TD></TR><TR><TD ALIGN='left'>"
    return String(s)

def end_row():
    s = f"</TD></TR>"
    return String(s)

def new_row():
    
    s = f"</TD></TR><TR><TD ALIGN='left'>"
    return String(s)

def record_end():
    return String("</TD></TR></TABLE>>")
#end.