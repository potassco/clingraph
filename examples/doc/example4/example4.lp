node(mike).

attr(node, mike, label, "<<b>{{name}} {{lastname}}</b>>").
attr(node, mike, (label,name), "Michel").
attr(node, mike, (label,lastname), "Scott").

node(jim).
attr(node, jim, (label,name), "Jim").
attr(node, jim, (label,lastname), "Halpert").

node(pam).
attr(node, pam, label, "<{{name['first']}} {{name['second']}} <b>{{lastname}}</b>>").
attr(node, pam, (label,name,first), "Pamela").
attr(node, pam, (label,name,second), "Morgan").
attr(node, pam, (label,lastname), "Beesly").

node(angela).
attr(node, angela, label, "<{%for k, n in name.items() %}{{n}} {% endfor %}<b>{{lastname}}</b>>").
attr(node, angela, (label,name,1), "Angela").
attr(node, angela, (label,name,2), "Noelle").
attr(node, angela, (label,lastname), "Martin").
