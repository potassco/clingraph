"""
Test  the Factbase
"""
#pylint: disable=missing-function-docstring
import pytest
from clingo import Control
from ..orm import Factbase
from ..utils import parse_clingo_json
from ..exceptions import InvalidSyntax

from .utils import get_example_file, get_example_str, make_file

# ------ Factbase

def test_init_default_graph():
    cg = Factbase()
    cg.add_fact_string("node(a).")
    assert "node(a,default)." in cg.get_facts()

    cg = Factbase(default_graph='other')
    cg.add_fact_string("node(a).")
    assert "node(a,other)." in cg.get_facts()

def test_init_prefix():
    cg = Factbase()
    cg.add_fact_string("pre_node(a).")
    assert not "pre_node(a,default)." in cg.get_facts()

    cg = Factbase(prefix='pre_')
    cg.add_fact_string("pre_node(a).")
    assert "pre_node(a,default)." in cg.get_facts()


def test_from_str():
    s = get_example_str(1)
    cg = Factbase()
    cg.add_fact_string(s)
    facts = cg.get_facts()
    assert 'node(john,default).' in facts
    assert 'node(jane,default).' in facts
    assert 'edge((john,jane),default).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

    cg = Factbase(default_graph='other')
    cg.add_fact_string(s)
    facts = cg.get_facts()
    assert 'node(john,other).' in facts
    assert 'node(jane,other).' in facts
    assert 'edge((john,jane),other).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

    cg = Factbase()
    with pytest.raises(InvalidSyntax):
        cg.add_fact_string("def sjs(): .node(a).")

    cg = Factbase.from_string(s)
    facts = cg.get_facts()
    assert 'node(john,default).' in facts
    assert 'node(jane,default).' in facts
    assert 'edge((john,jane),default).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

    cg = Factbase.from_string(s, default_graph='other')
    facts = cg.get_facts()
    assert 'node(john,other).' in facts
    assert 'node(jane,other).' in facts
    assert 'edge((john,jane),other).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

def test_from_file():
    s = get_example_file(1)
    cg = Factbase()
    cg.add_fact_file(s)
    facts = cg.get_facts()
    assert 'node(john,default).' in facts
    assert 'node(jane,default).' in facts
    assert 'edge((john,jane),default).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

    cg = Factbase(default_graph='other')
    cg.add_fact_file(s)
    facts = cg.get_facts()
    assert 'node(john,other).' in facts
    assert 'node(jane,other).' in facts
    assert 'edge((john,jane),other).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

    cg = Factbase()
    file_name = make_file("def: __init__()")
    with pytest.raises(InvalidSyntax):
        cg.add_fact_file(file_name)

def test_from_model():
    cg = Factbase()
    ctl = Control(["-n2"])
    ctl.add("base", [], "1{node(a);node(b)}1.")
    ctl.ground([("base", [])])
    ctl.solve(on_model=cg.add_model)
    facts = cg.get_facts()
    assert 'node(a,default).' in facts
    assert 'node(b,default).' in facts
    #pylint: disable=duplicate-code
    fbs = []
    ctl = Control(["-n2"])
    ctl.add("base", [], "1{node(a);node(b)}1.")
    ctl.ground([("base", [])])
    ctl.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))
    assert 'node(a,default).' in fbs[0].get_facts()
    assert 'node(a,default).' not in fbs[1].get_facts()
    assert 'node(b,default).' in fbs[1].get_facts()
    assert 'node(b,default).' not in fbs[0].get_facts()

def test_missing_graph():
    s = "node(n).graph(h,g)."
    cg = Factbase(default_graph='g')
    cg.add_fact_string(s)
    facts = cg.get_facts()
    graphs = cg.get_all_graphs()
    cg.get_graph_elements('node',graphs[0])


def test_from_json():

    json = '''
    {
        "Call": [{"Witnesses": [
                {"Value": ["attr(node,a,color,blue)", "node(a)"]},
                {"Value": ["attr(node,b,color,red)", "node(b)"]}]
            }],
        "Result": "SATISFIABLE"
        }
    '''
    models_prgs = parse_clingo_json(json)
    assert len(models_prgs) == 2
    fbs = [Factbase.from_string(prg) for prg in models_prgs]
    assert 'node(a,default).' in fbs[0].get_facts()
    assert 'node(b,default).' in fbs[1].get_facts()


    json = '''
    {
        "Missing Call": 1
        }
    '''
    with pytest.raises(InvalidSyntax):
        parse_clingo_json(json)


    json = '''
    {
        "Call": 1}
    '''
    with pytest.raises(InvalidSyntax):
        parse_clingo_json(json)

    json = '''
    {
        "Call": []}
    '''

    with pytest.raises(InvalidSyntax):
        parse_clingo_json(json)

    json = '''
    {
        "Call": [{"Missing Wit":1}]}
    '''
    with pytest.raises(InvalidSyntax):
        parse_clingo_json(json)
