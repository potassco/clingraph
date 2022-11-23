node(ID) :- employee(ID,_,_,_).
attr(node, ID, label, """<<b>{{name}} {{lastname}}</b><br/>
                        <i>({{area}})</i>>"""):-node(ID).
attr(node, ID, (label,name), Name):-employee(ID,Name,_,_).
attr(node, ID, (label,lastname), Lastname):-employee(ID,_,Lastname,_).
attr(node, ID, (label,area), Area):-employee(ID,_,_,Area).
attr(graph, default, label, "The Office").