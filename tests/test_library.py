import os
import shutil
import pytest
from graphviz import Graph, Digraph
from clingraph import Clingraph, InvalidSyntax
from clingraph import MultiModelClingraph
from clingo import Control

# ------ Utils
def get_example_file(number):
    return os.path.join("examples","basic",f"example{number}",f"example_{number}.lp")

def get_example_str(number):
    with open(get_example_file(number), 'r') as lpfile:
        return lpfile.read()

def make_file(content):
    if not os.path.exists('out'):
        os.makedirs('out')
    with open('out/test_tmp.lp', 'w') as lpfile:
        lpfile.write(content)

    return 'out/test_tmp.lp'

def clean_out():
    folder = 'out'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

# -----


def test_init_default_graph():
    cg = Clingraph()
    cg.add_fact_string("node(a).")
    assert not cg._computed
    assert "node(a,default)." in cg.get_facts()

    cg = Clingraph(default_graph='other')
    cg.add_fact_string("node(a).")
    assert not cg._computed
    assert "node(a,other)." in cg.get_facts()

def test_init_prefix():
    cg = Clingraph()
    cg.add_fact_string("pre_node(a).")
    assert not "pre_node(a,default)." in cg.get_facts()

    cg = Clingraph(prefix='pre_')
    cg.add_fact_string("pre_node(a).")
    assert "pre_node(a,default)." in cg.get_facts()

def test_init_type():
    cg = Clingraph()
    g = cg._new_single_graph()
    assert type(g) == Graph

    cg = Clingraph(type_='digraph')
    g = cg._new_single_graph()
    assert type(g) == Digraph


def test_from_str():
    s = get_example_str(1)
    cg = Clingraph()
    cg.add_fact_string(s)
    facts = cg.get_facts()
    assert 'node(john,default).' in facts
    assert 'node(jane,default).' in facts
    assert 'edge((john,jane),default).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

    cg = Clingraph(default_graph='other')
    cg.add_fact_string(s)
    facts = cg.get_facts()
    assert 'node(john,other).' in facts
    assert 'node(jane,other).' in facts
    assert 'edge((john,jane),other).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

    cg = Clingraph()
    with pytest.raises(InvalidSyntax):
        cg.add_fact_string("def sjs(): .node(a).")



def test_from_file():
    s = get_example_file(1)
    cg = Clingraph()
    cg.add_fact_file(s)
    facts = cg.get_facts()
    assert 'node(john,default).' in facts
    assert 'node(jane,default).' in facts
    assert 'edge((john,jane),default).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

    cg = Clingraph(default_graph='other')
    cg.add_fact_file(s)
    facts = cg.get_facts()
    assert 'node(john,other).' in facts
    assert 'node(jane,other).' in facts
    assert 'edge((john,jane),other).' in facts
    assert 'attr(graph,default,(label,-1),"Does family").' in facts
    assert 'attr(graph_nodes,default,(style,-1),filled).' in facts
    assert 'attr(node,john,(label,-1),"John Doe").' in facts
    assert 'attr(node,jane,(label,-1),"Jane Doe").' in facts

    cg = Clingraph()
    file_name = make_file("def: __init__()")
    with pytest.raises(InvalidSyntax):
        cg.add_fact_file(file_name)

def test_from_model():
    cg = Clingraph()
    ctl = Control(["-n2"])
    ctl.add("base", [], "1{node(a);node(b)}1.")
    ctl.ground([("base", [])])
    ctl.solve(on_model=cg.add_model)
    facts = cg.get_facts()
    assert 'node(a,default).' in facts
    assert 'node(b,default).' in facts

def test_from_get_graphviz():
    cg = Clingraph()
    cg.add_fact_string("node(a).node(b,other).graph(other).")
    with pytest.raises(RuntimeError):
        cg.get_graphviz()
    cg.compute_graphs()
    assert cg.get_graphviz().name == 'default'
    assert cg.get_graphviz('default').name == 'default'
    assert cg.get_graphviz('other').name == 'other'
    with pytest.raises(ValueError):
        cg.get_graphviz('wrong')

    cg = Clingraph(default_graph ='other')
    cg.add_fact_string("node(b,other).graph(other).")
    cg.compute_graphs()
    assert cg.get_graphviz().name == 'other'


def test_source():
    s = get_example_file(1)
    cg = Clingraph()
    cg.add_fact_file(s)
    cg.compute_graphs()
    source = cg.source()

    assert "graph default {" in source
    assert 'graph [label="Does family"]' in source
    assert 'node [style=filled]' in source
    assert 'jane [label="Jane Doe"]' in source
    assert 'john [label="John Doe"]' in source
    assert 'john -- jane' in source


    s = get_example_file(2)
    cg = Clingraph()
    cg.add_fact_file(s)
    cg.compute_graphs()
    source = cg.source()

    assert '//----------toms_family----------' in source
    assert 'graph toms_family {' in source
    assert 'tom' in source
    assert 'max' in source
    assert 'tom -- max' in source
    assert '//----------bills_family----------' in source
    assert 'graph bills_family {' in source
    assert 'bill' in source
    assert 'jen' in source
    assert 'bill -- jen' in source
    assert '}' in source



    s = get_example_file(3)
    cg = Clingraph()
    cg.add_fact_file(s)
    cg.compute_graphs()
    source = cg.source()

    assert 'graph house {' in source
    assert '	graph [label="Tom\'s House"]' in source
    assert '	node [color=cyan style=filled]' in source
    assert '	toilet -- bed [color=red]' in source
    assert '	subgraph cluster_bathroom {' in source
    assert '		graph [label=Bathroom style=dotted]' in source
    assert '		toilet [shape=circle]' in source
    assert '	subgraph cluster_bedroom {' in source
    assert '		graph [label=Bedroom style=dotted]' in source
    assert '		bed [shape=square]' in source
    assert '		desk [shape=square]' in source


    s = get_example_file(4)
    cg = Clingraph()
    cg.add_fact_file(s)
    cg.compute_graphs()
    source = cg.source()

    assert 'graph default {' in source
    assert '	mike [label="Michel Scott"]' in source
    assert '	toby' in source
    label_in = False
    label_in |= '	mike -- toby [label="enemy-hate-boss"]' in source
    label_in |= '	mike -- toby [label="enemy-boss-hate"]' in source
    label_in |= '	mike -- toby [label="boss-enemy-hate"]' in source
    label_in |= '	mike -- toby [label="boss-hate-enemy"]' in source
    label_in |= '	mike -- toby [label="hate-enemy-boss"]' in source
    label_in |= '	mike -- toby [label="hate-boss-enemy"]' in source

    assert label_in
    assert '}' in source


def test_save():
    clean_out()
    s = get_example_file(1)
    cg = Clingraph()
    cg.add_fact_file(s)
    cg.compute_graphs()
    cg.save(directory ='out')
    assert os.path.isfile(os.path.join('out','default.pdf'))

    clean_out()
    s = get_example_file(1)
    cg = Clingraph(default_graph ='other')
    cg.add_fact_file(s)
    cg.compute_graphs()
    cg.save(directory ='out')
    assert os.path.isfile(os.path.join('out','other.pdf'))

    clean_out()
    s = get_example_file(2)
    cg = Clingraph()
    cg.add_fact_file(s)
    cg.compute_graphs()
    cg.save(directory ='out')
    assert os.path.isfile('out/bills_family.pdf')
    assert os.path.isfile(os.path.join('out','toms_family.pdf'))

    clean_out()
    s = get_example_file(2)
    cg = Clingraph()
    cg.add_fact_file(s)
    cg.compute_graphs()
    cg.save(directory ='out', selected_graphs=['bills_family'])
    assert os.path.isfile(os.path.join('out','bills_family.pdf'))
    assert not os.path.isfile(os.path.join('out','toms_family.pdf'))

    clean_out()
    s = get_example_file(3)
    cg = Clingraph()
    cg.add_fact_file(s)
    cg.compute_graphs()
    cg.save(directory ='out',format='png')
    assert os.path.isfile(os.path.join('out','house.png'))

    clean_out()
    cg.save(directory ='out',format='svg')
    assert os.path.isfile(os.path.join('out','house.svg'))

    clean_out()
    cg.save(directory ='out',format='svg',name_prefix='pre_')
    assert os.path.isfile(os.path.join('out','pre_house.svg'))

    s = get_example_file(3)
    cg = Clingraph()
    cg.add_fact_file(s)
    with pytest.raises(RuntimeError):
        cg.save()


def test_multi_model():
    cg = MultiModelClingraph()
    ctl = Control(["-n2"])
    ctl.add("base", [], get_example_str(5))
    ctl.ground([("base", [])])
    ctl.solve(on_model=cg.add_model)

    assert list(cg.clingraphs.keys())==[1,2]
    assert 'node(a,default).' in cg.get_clingraph(1).get_facts()
    assert 'node(b,default).' in cg.get_clingraph(2).get_facts()

    cg.compute_graphs()
    assert cg.get_clingraph(1)._computed
    assert cg.get_clingraph(2)._computed

    assert 'a [color=blue]' in cg.get_clingraph(1).source()
    assert 'b [color=red]' in cg.get_clingraph(2).source()

    cg = MultiModelClingraph(default_graph='other')
    ctl = Control(["-n2"])
    ctl.add("base", [], get_example_str(5))
    ctl.ground([("base", [])])
    ctl.solve(on_model=cg.add_model)

    cg.compute_graphs()

    clean_out()
    cg.save(format='svg')
    assert os.path.isfile(os.path.join('out','model-0001','other.svg'))
    assert os.path.isfile(os.path.join('out','model-0002','other.svg'))

    clean_out()
    cg.save(format='svg',selected_models=[1])
    assert os.path.isfile(os.path.join('out','model-0001','other.svg'))
    assert not os.path.isfile(os.path.join('out','model-0002','other.svg'))


    json = '''
    {
        "Call": [{"Witnesses": [
                {"Value": ["attr(node,a,color,blue)", "node(a)"]},
                {"Value": ["attr(node,b,color,red)", "node(b)"]}]
            }]}
    '''
    cg = MultiModelClingraph()
    cg.load_json(json)

    assert list(cg.clingraphs.keys())==[1,2]
    assert 'node(a,default).' in cg.get_clingraph(1).get_facts()
    assert 'node(b,default).' in cg.get_clingraph(2).get_facts()

    cg.compute_graphs()
    assert cg.get_clingraph(1)._computed
    assert cg.get_clingraph(2)._computed

    assert 'a [color=blue]' in cg.get_clingraph(1).source()
    assert 'b [color=red]' in cg.get_clingraph(2).source()

    json = '''
    {
        "Missing Call": 1
        }
    '''
    cg = MultiModelClingraph()
    with pytest.raises(InvalidSyntax):
        cg.load_json(json)


    json = '''
    {
        "Call": 1}
    '''
    with pytest.raises(InvalidSyntax):
        cg.load_json(json)

    json = '''
    {
        "Call": []}
    '''

    with pytest.raises(InvalidSyntax):
        cg.load_json(json)

    json = '''
    {
        "Call": [{"Missing Wit":1}]}
    '''
    with pytest.raises(InvalidSyntax):
        cg.load_json(json)
