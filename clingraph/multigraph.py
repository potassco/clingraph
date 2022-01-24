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
    Holds multiple models in the same structure.
    Special addaptation for the ouypuy of clingo
    """

    def __init__(self, **kargs):
        """
        Constructs a new multi model clingraph
        """
        self.clingraphs = {}
        self.new_clingraph = lambda: Clingraph(**kargs)

    def __str__(self):
        """
        String representation
        """
        return self.source()

    def name(self, number, costs):
        """
        Returns the name of a clingraph related to a model
        Arguments:
            numeber (int): The model number. Will be used to access the model
            costs (list): A list of costs for the model
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
        Obtains the source dot code for the models.
        A selecttion is also allowed as parameters, if no selection is
        add all models and graphs are returned
        Optional arguments:
            selected_graphs (list): List of the names of the graphs to be selected
            selected_models (list): List of the model names to be selected
        """

        s = ""
        if not selected_models:
            selected_models = self.clingraphs.keys()
        for m_num in selected_models:
            if m_num not in self.clingraphs:
                LOG.warn(f'Invalid model number: {m_num}')
                continue
            g_dic = self.clingraphs[m_num]
            s += "\n//"+"="*25 + "\n"
            s += f"//\tModel: {m_num} Costs: {g_dic['costs']} \n"
            s += "//"+"="*25 + "\n\n"
            s += g_dic["clingraph"].source(selected_graphs=selected_graphs)
        return s

    def get_cligraph(self, model_number):
        """
        Returns the clingraph associated to the model number
        Arguments:
            model_number: The model number to be obtained
        """
        if not model_number in self.clingraphs:
            raise ValueError("Invalid model number")
        return self.clingraphs[model_number]['clingraph']

    def add_model(self, model):
        """
        Adds a new clingraph based on a clingo model
        Arguments:
            model (clingo.Model): A model returned by clingos solver
        """
        g = self.new_clingraph()
        g.add_model(model)
        name = self.name(model.number, model.cost)
        self.clingraphs[model.number] = {
            "clingraph": g,
            "name": name,
            "costs": model.cost}

    def load_json(self, json_str):
        """
        Loads multiple models from a json that is the output of clingo
        The json oput is obtained using the option `--outf=2`
        Arguments:
            json_str (str): A string representing the json
        """
        j = json.loads(json_str)
        LOG.debug(f"Loading json {json.dumps(j)}")
        for i, w in enumerate(j["Call"][0]["Witnesses"]):
            prg_str = "\n".join([f"{v}." for v in w["Value"]])
            g = self.new_clingraph()
            g.add_fact_string(prg_str)
            costs = [] if not "Costs" in w else w["Costs"]
            name = self.name(i, costs)
            self.clingraphs[i] = {
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
        Arguments:
            directory (str): The directory for the outpus
        """
        for g_dic in self.clingraphs.values():
            new_directory = os.path.join(directory, g_dic['name'])
            g_dic['clingraph'].save(new_directory, **kargs)
