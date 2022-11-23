"""
Test Graphviz
"""
#pylint: disable=missing-function-docstring
import os
from graphviz import Graph, Digraph
from clingo import Control
from .. import Factbase
from ..graphviz import compute_graphs, dot, render
from ..gif import save_gif
from ..tex import tex
from ..utils import write
from .utils import get_example_file, clean_out
from ..clingo_utils import add_elements_ids, add_svg_interaction, ClingraphContext

def test_compute_graphs():
    cg = Factbase()
    cg.add_fact_string("node(a).node(b,other).graph(other).")
    graphs = compute_graphs(cg)
    assert 'default' in graphs
    default = graphs['default']
    other = graphs['other']
    assert default.name == 'default'
    assert other.name == 'other'

    cg = Factbase(default_graph ='other')
    cg.add_fact_string("node(a).node(b,other).graph(other).")
    graphs = compute_graphs(cg)
    assert list(graphs.keys())==['other']
    assert isinstance(graphs['other'], Graph)

    cg = Factbase(default_graph ='other')
    cg.add_fact_string("node(a).node(b,other).graph(other).")
    graphs = compute_graphs(cg,graphviz_type='digraph')
    assert list(graphs.keys())==['other']
    assert isinstance(graphs['other'], Digraph)

def test_dot():
    s = get_example_file(1)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    source = dot(graphs)
    default_source = source['default']
    assert "graph default {" in default_source
    assert 'graph [label="Does family"]' in default_source
    assert 'node [style=filled]' in default_source
    assert 'jane [label="Jane Doe"]' in default_source
    assert 'john [label="John Doe"]' in default_source
    assert 'john -- jane' in default_source


    s = get_example_file(2)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    source = dot(graphs)
    toms_family = source['toms_family']

    assert 'graph toms_family {' in toms_family
    assert 'tom' in toms_family
    assert 'max' in toms_family
    assert 'tom -- max' in toms_family

    bills_family = source['bills_family']

    assert 'graph bills_family {' in bills_family
    assert 'bill' in bills_family
    assert 'jen' in bills_family
    assert 'bill -- jen' in bills_family
    assert '}' in bills_family



    s = get_example_file(3)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    source = dot(graphs)
    house = source['house']

    assert 'graph house {' in house
    assert '	graph [label="Tom\'s House"]' in house
    assert '	node [color=cyan style=filled]' in house
    assert '	toilet -- bed [color=red]' in house
    assert '	subgraph cluster_bathroom {' in house
    assert '		graph [label=Bathroom style=dotted]' in house
    assert '		toilet [shape=circle]' in house
    assert '	subgraph cluster_bedroom {' in house
    assert '		graph [label=Bedroom style=dotted]' in house
    assert '		bed [shape=square]' in house
    assert '		desk [shape=square]' in house


    s = get_example_file(4)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    source = dot(graphs)
    default = source['default']

    assert 'graph default {' in default
    assert '	mike [label=<<b>Michel Scott</b>>]' in default
    assert '	pam [label=<Pamela Morgan <b>Beesly</b>>]' in default
    assert '	angela [label=<Angela Noelle <b>Martin</b>>]' in default
    assert '	jim [label=HalpertJim]' in default 

    assert '}' in default

def test_render():
    clean_out()
    s = get_example_file(1)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    paths = render(graphs, directory ='out')
    assert os.path.join('out','default.pdf') == paths['default']
    assert os.path.isfile(os.path.join('out','default.pdf'))

    clean_out()
    s = get_example_file(1)
    cg = Factbase(default_graph ='other')
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    paths = render(graphs, directory ='out')
    assert os.path.join('out','other.pdf') == paths['other']
    assert os.path.isfile(os.path.join('out','other.pdf'))

    clean_out()
    s = get_example_file(2)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    paths = render(graphs, directory ='out')
    assert os.path.join('out','bills_family.pdf') == paths['bills_family']
    assert os.path.join('out','toms_family.pdf') == paths['toms_family']

    assert os.path.isfile(os.path.join('out','bills_family.pdf'))
    assert os.path.isfile(os.path.join('out','toms_family.pdf'))

    clean_out()
    s = get_example_file(2)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    selected_graphs = {k:graphs[k] for k in ['bills_family']}
    paths = render(selected_graphs, directory ='out')
    assert os.path.isfile(os.path.join('out','bills_family.pdf'))
    assert not os.path.isfile(os.path.join('out','toms_family.pdf'))

    clean_out()
    s = get_example_file(3)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    paths = render(graphs, directory ='out',format='png')
    assert os.path.isfile(os.path.join('out','house.png'))

    clean_out()
    paths = render(graphs, directory ='out',format='svg')
    assert os.path.isfile(os.path.join('out','house.svg'))

    clean_out()
    paths = render(graphs, directory ='out',format='svg',name_format='pre_{graph_name}')
    assert os.path.isfile(os.path.join('out','pre_house.svg'))


def test_gif():
    s = get_example_file(2)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    clean_out()
    save_gif(graphs)
    assert os.path.isfile(os.path.join('out','movie.gif'))
    assert os.path.isfile(os.path.join('out','images','gif_image_bills_family_0.png'))
    assert os.path.isfile(os.path.join('out','images','gif_image_toms_family_0.png'))

    clean_out()
    save_gif(graphs,name_format='{graph_name}-{model_number}')
    assert os.path.isfile(os.path.join('out','movie-0.gif'))
    assert os.path.isfile(os.path.join('out','images','gif_image_bills_family_0.png'))
    assert os.path.isfile(os.path.join('out','images','gif_image_toms_family_0.png'))


def test_tex():
    s = get_example_file(6)
    cg = Factbase()
    cg.add_fact_file(s)
    graphs = compute_graphs(cg)
    clean_out()
    texs = tex(graphs)
    assert r'node {$\forall x\in \Theta$}' in texs['default']
    paths = write(texs,'out',format='tex')
    assert paths['default'] == os.path.join('out','default.tex')
    assert os.path.isfile(os.path.join('out','default.tex'))



def test_multi_model():
    clean_out()
    #pylint: disable=duplicate-code
    fbs = []
    ct = Control(["-n2"])
    ct.add("base", [], "1{node(a);node(b)}1.")
    ct.ground([("base", [])])
    ct.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))
    multi_graphs = compute_graphs(fbs)
    some_graphs = [None,multi_graphs[1]]
    assert len(multi_graphs) == 2
    assert list(multi_graphs[0].keys())==['default']
    assert list(multi_graphs[1].keys())==['default']
    assert isinstance(multi_graphs[0]['default'], Graph)
    assert isinstance(multi_graphs[1]['default'], Graph)

    source = dot(multi_graphs)
    assert 'graph default {' in source[0]['default']
    assert 'graph default {' in source[1]['default']

    source = dot(some_graphs)
    assert source[0] is None
    assert 'graph default {' in source[1]['default']


    render(multi_graphs,directory ='out',format='pdf',name_format='pre_{graph_name}_{model_number}')
    assert os.path.isfile(os.path.join('out','pre_default_0.pdf'))
    assert os.path.isfile(os.path.join('out','pre_default_1.pdf'))

    clean_out()
    render(some_graphs,directory ='out',format='pdf',name_format='pre_{graph_name}_{model_number}')
    assert not os.path.isfile(os.path.join('out','pre_default_0.pdf'))
    assert os.path.isfile(os.path.join('out','pre_default_1.pdf'))

    clean_out()
    save_gif(multi_graphs,directory ='out',name_format='{graph_name}_{model_number}')
    assert os.path.isfile(os.path.join('out','images','gif_image_default_0.png'))
    assert os.path.isfile(os.path.join('out','images','gif_image_default_1.png'))
    assert os.path.isfile(os.path.join('out','movie_0.gif'))
    assert os.path.isfile(os.path.join('out','movie_1.gif'))

    clean_out()
    save_gif(some_graphs,directory ='out',name_format='{graph_name}_{model_number}')
    assert not os.path.isfile(os.path.join('out','images','gif_image_default_0.png'))
    assert os.path.isfile(os.path.join('out','images','gif_image_default_1.png'))
    assert not os.path.isfile(os.path.join('out','movie_0.gif'))
    assert os.path.isfile(os.path.join('out','movie_1.gif'))


    clean_out()
    texs = tex(multi_graphs)
    write(texs,'out',format='tex',name_format="{model_number}/{graph_name}")
    assert os.path.isfile(os.path.join('out','0','default.tex'))
    assert os.path.isfile(os.path.join('out','1','default.tex'))


def test_svg():

    fbs = []
    ctl = Control(['--warn=none'])
    add_elements_ids(ctl)
    ctl.load(get_example_file(7))
    ctl.ground([("base", [])],ClingraphContext())
    ctl.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))
    graphs = compute_graphs(fbs)
    paths = render(graphs,directory ='out',format='svg')
    add_svg_interaction(paths)
    with open(os.path.join('out','default.svg'),'r',encoding="UTF8") as f:
        s = f.read()
        assert '</script>' in s
        assert 'init___visibility___hidden' in s
        assert 'mouseleave___4___color___blue' in s
        assert 'click___3___visibility___visible' in s
        assert 'fill="currentcolor"' in s
