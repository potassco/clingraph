from clingo.application import Application
import graphviz

class Clingraph(Application):
    program_name = 'clingraph'
    version = '0.1.0-dev'

    def main(self, ctl, files):
        for path in files:
            ctl.load(path)
        if not files:
            ctl.load('-')
        ctl.ground([('base', [])], context=self)
        ctl.solve()

    def print_model(self, model, printer):
        # TODO: Build the graph here using graphviz
        pass
