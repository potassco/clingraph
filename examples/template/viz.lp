person(anna). name(anna,"Anna"). middlename(anna,"Julia"). lastname(anna,"Scott").
person(tom). name(tom,"Thomas"). lastname(tom,"Blake").

node(N):-person(N).
attr(node,N,shape,none):-person(N).
attr(node,N,label,@concat("<<table>",
                            "<tr><td><b>{{id}}</b></td></tr>",
                            "<tr><td>{{lastname}} ({{name['first']}} {{name['middle']}})</td></tr>",
                        "</table>>")):-person(N).
attr(node,N,(label,id),N):-name(N,Name).
attr(node,N,(label,name,first),Name):-name(N,Name).
attr(node,N,(label,name,middle),Name):-middlename(N,Name).
attr(node,N,(label,lastname),Lastname):-lastname(N,Lastname).