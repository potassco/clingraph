"""
    Definition of a MultiModelClingraph
"""
import os
import logging
import json
from clingraph import Clingraph
LOG = logging.getLogger('custom')


class MultiModelClingraph:
    """
    Holds multiple models in the same structure. Each model will be associated with a :py:class:`Clingraph` object.
    
    The class is specially intended for integration with clingo.
    """

    def __init__(self, **kargs):
        """
        Constructs a new multi model clingraph. 
        Accepts all the arguments in the :py:class:`Clingraph` constructor which will be used in the creation of each :py:class:`Clingraph` object.
        """
        self.clingraphs = {}
        self._new_clingraph = lambda: Clingraph(**kargs)

    def __str__(self):
        """
        String representation
        """
        return self.source()

    def _name(self, number, costs):
        """
        Returns the name of a clingraph related to a model
        
        Args:
            numeber (int): The model number. Will be used to access the model
            costs (list): A list of costs for the model
        
        Returns:
            The name of a clingraph related to a model and cost
        """
        cost_name = ""
        for cost in costs:
            cost_name += f"-{cost}"
        if cost_name != "":
            cost_name = "cost"+cost_name+"__"
        name = f"{cost_name}model-{number:04d}"
        return name

    def source(self, selected_graphs=None, selected_models=None):
        """
        Obtains the source code for the graphs in all the models.
        A selecttion is also allowed as parameters, if no selection is
        added all models and graphs are returned.
        
        Args:
            selected_graphs (list): List of the names of the graphs to be selected
            selected_models (list): List of the model numbers to be selected

        Returns:
            A string containing the source graphviz code of the selected models and graphs.
        """

        s = ""
        if not selected_models:
            selected_models = self.clingraphs.keys()
        for m_num in selected_models:
            m_num=int(m_num)
            if m_num not in self.clingraphs:
                LOG.warn(f'Invalid model number: {m_num}')
                continue
            g_dic = self.clingraphs[m_num]
            s += "\n//"+"="*25 + "\n"
            s += f"//\tModel: {m_num} Costs: {g_dic['costs']} \n"
            s += "//"+"="*25 + "\n\n"
            s += g_dic["clingraph"].source(selected_graphs=selected_graphs)
        return s

    def get_clingraph(self, model_number):
        """
        Returns the clingraph associated to the model number
        
        Args:
            model_number: The model number to be obtained

        Returns:
            A :py:class:`Clingraph` object associated to the model number
        """
        model_number = int(model_number)
        if not model_number in self.clingraphs:
            raise ValueError("Invalid model number")
        return self.clingraphs[model_number]['clingraph']

    def add_model(self, model):
        """
        Creates a new clingraph based on a clingo model.
        
        Args:
            model (clingo.Model): A model returned by clingos solver

        Example:
            Create a multi model clingraph using clingos API::

                from clingraph import MultiModelClingraph
                from clingo import Control
                ctl = Control(["-n2"])
                g = MultiModelClingraph()
                ctl.add("base", [], "1{node(a);node(b)}1.")
                ctl.ground([("base", [])])
                ctl.solve(on_model=g.add_model)
        """
        g = self._new_clingraph()
        g.add_model(model)
        name = self._name(model.number, model.cost)
        self.clingraphs[int(model.number)] = {
            "clingraph": g,
            "name": name,
            "costs": model.cost}

    def load_json(self, json_str):
        """
        Loads multiple models from a json that is the output of clingo
        The json oput is obtained using the option `--outf=2`
        
        Args:
            json_str (str): A string representing the json
        """
        j = json.loads(json_str)
        LOG.debug(f"Loading json {json.dumps(j)}")
        for i, w in enumerate(j["Call"][0]["Witnesses"]):
            model_number = i+1
            prg_str = "\n".join([f"{v}." for v in w["Value"]])
            g = self._new_clingraph()
            g.add_fact_string(prg_str)
            costs = [] if not "Costs" in w else w["Costs"]
            name = self._name(model_number, costs)
            self.clingraphs[model_number] = {
                "clingraph": g,
                "name": name,
                "costs": costs}

    def compute_graphs(self):
        """
        Computes all the clingraphs
        """
        for g_dic in self.clingraphs.values():
            g_dic['clingraph'].compute_graphs()

    def save(self, directory, **kargs):
        """
        Saves all the clingraphs using one directory per model
        
        Args:
            directory (str): The directory for the outpus
        """
        for g_dic in self.clingraphs.values():
            new_directory = os.path.join(directory, g_dic['name'])
            g_dic['clingraph'].save(new_directory, **kargs)
