from benchmarks_conf import get_nsga2_toolbox, get_frams_toolbox

EXPERIMENTS = {
    "dtlz1": get_nsga2_toolbox,
    "dtlz2": get_nsga2_toolbox,
    "dtlz3": get_nsga2_toolbox,
    "dtlz4": get_nsga2_toolbox,
    "frams": get_frams_toolbox
}


class Experiment:

    def __init__(self, experiment_name: str, *args):

        self.toolbox = EXPERIMENTS[experiment_name](experiment_name, *args)

