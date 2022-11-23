#script (python)
import sys
import time
from clingraph import Factbase, compute_graphs, render
from clingraph.clingo_utils import ClingraphContext
from clingraph.gif import save_gif
from clingo import Control

class ClingraphPropagator:
    def __init__(self, viz_encoding):
        self.viz_encoding = viz_encoding
        self.factbases = []
        self.l2s = {}

    def init(self, init):
        for atom in init.symbolic_atoms:
            lit = init.solver_literal(atom.literal)
            self.l2s.setdefault(lit, []).append(str(atom.symbol))
            init.add_watch(lit)

    def propagate(self, ctl, changes):
        i = len(self.factbases)
        propagation_prg = [f"_step_type(propagate,{i}).",
                           f"_level({ctl.assignment.decision_level})."]
        for l,symbols in self.l2s.items():
            v = ctl.assignment.value(l)
            t = '_undefined' if v is None else '_true' if v else '_false'
            for s in symbols:
                propagation_prg.append(f"{t}({s}).")
        for l in changes:
            symbols = self.l2s[l]
            for s in symbols:
                propagation_prg.append(f"_change({s}).")
        self.add_factbase(propagation_prg)
        return True

    def undo(self, solver_id, assign, undo):
        i = len(self.factbases)
        propagation_prg = [f"_step_type(undo,{i}).", f"_level({assign.decision_level})."]

        for l,symbols in self.l2s.items():
            v = assign.value(l)
            t = '_undefined' if v is None else '_true' if v else '_false'
            for s in symbols:
                propagation_prg.append(f"{t}({s}).")
        for l in undo:
            symbols = self.l2s[l]
            for s in symbols:
                propagation_prg.append(f"_change({s}).")

        self.add_factbase(propagation_prg)

    def decide(self, thread_id, assign, fallback):
        i = len(self.factbases)
        propagation_prg = [f"_step_type(decide,{i}).", f"_level({assign.decision_level})."]

        for l,symbols in self.l2s.items():
            v = assign.value(l)
            t = '_undefined' if v is None else '_true' if v else '_false'
            for s in symbols:
                propagation_prg.append(f"{t}({s}).")
        if abs(fallback) in self.l2s:
            for s in self.l2s[abs(fallback)]:
                pol = "pos" if fallback > 0 else "neg"
                propagation_prg.append(f"_decide({s},{pol}).")

        self.add_factbase(propagation_prg)
        return 0

    def add_factbase(self, prg_list):
        fb = Factbase()
        ctl = Control([])
        ctl.load(self.viz_encoding)
        ctl.add("base",[],"".join(prg_list))
        ctl.ground([("base",[])],ClingraphContext())
        ctl.solve(on_model=fb.add_model)
        self.factbases.append(fb)

def main(prg):
    viz_encoding = './examples/propagator/sudoku/viz-sudoku-solving.lp'
    prop = ClingraphPropagator(viz_encoding)
    prg.register_propagator(prop)
    prg.ground([("base", [])])
    prg.solve()
    graphs = compute_graphs(prop.factbases)
    all_graphs = {}
    for d in graphs:
        all_graphs.update(d)
        render(d,format='pdf',engine='neato')
    save_gif(all_graphs,engine='neato',fps='0.5')
#end.


