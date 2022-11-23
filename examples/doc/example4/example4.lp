node(mike).

% attr(node, mike, label, "<<b>{{name}} {{lastname}}<\b>>").
% attr(node, mike, (label,name), "Michel").
% attr(node, mike, (label,lastname), "Scott").

% node(jim).
% attr(node, jim, (label,name), "Jim").
% attr(node, jim, (label,lastname), "Halpert").

node(pam).


% attr(node, pam, label, "{%for n in name %}{{n}} {% endfor %}<b>{{lastname}}<\b>").
attr(node, pam, (label,name), "Pamela").
% attr(node, pam, (label,name), "Morgan").
attr(node, pam, (label,lastname), "Beesly").
% data = {'name':{Pamela,Morgan}, 'lastname':"Beesley"}
% output = 'Pamela Morgan <b>Beesley<\b>'

% data = {'lastname':"Beesley"}
% output = '<b>Beesley<\b>'

% attr(node, pam, (label,name), "Pamela").
% attr(node, pam, (label,lastname), "Beesly").
% data = {'name':'Pamela', 'lastname':"Beesley"}
% output = 'P a m e l a <b>Beesley<\b>'


attr(node, pam, label, "{% set ns = name|default({}) %} {{ns}}").
"{% if name is string %} {% set name = {} %} {% endif %}"
% attr(node, pam, label, "{%for n in name.values() %}{{n}} {% endfor %}{{lastname}}").
% attr(node, pam, (label,name,first), "Pamela").
% attr(node, pam, (label,name,second), "Morgan").
% attr(node, pam, (label,lastname), "Beesly").
% data = {'name':{'first':"Pamela",second:"Beesley"}, 'lastname':"Beesley"}


% edge((mike,jim)).
% edge((mike,pam)).
% edge((jim,pam)).

% attr(edge, (mike,jim), label, "{% if area %}AREA: {{area}} {%else%} ?{% endif %}").
% attr(edge, (mike,jim), (label,area), "sales").

% attr(edge, (mike,pam), label, "{% if area %}AREA: {{area}} {%else%} ?{% endif %}").

% attr(edge, (jim,pam), label, "{% for v in data.values()%}{{v}} {% endfor %}").
% attr(edge, (jim,pam), (label,1), "co-worker").
% attr(edge, (jim,pam), (label,2), "married").