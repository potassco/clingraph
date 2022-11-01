node(1..4).
edge((1,2..3)).
edge((3,4)).

attr(node,N,style,filled):-node(N).
attr(node,N,fillcolor,@svg_color()):-node(N).
attr(node,N,class,@svg_init(visibility,hidden)):-node(N), N!=1.  
attr(node,N,class,@svg_init(color,blue)):-node(N).  
attr(node,N2,class,@svg(click,N1,visibility,visible)):-edge((N1,N2)).    
attr(node,N,class,@svg(mouseenter,N,color,green)):-node(N).
attr(node,N,class,@svg(mouseleave,N,color,blue)):-node(N).