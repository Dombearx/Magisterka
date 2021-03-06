from benchmarks_conf import get_nsga2_toolbox, get_frams_nsga2_toolbox, get_one_criteria_toolbox, get_frams_one_criteria_toolbox

EXPERIMENTS = {
    "dtlz1": get_nsga2_toolbox,
    "dtlz2": get_nsga2_toolbox,
    "dtlz3": get_nsga2_toolbox,
    "dtlz4": get_nsga2_toolbox,
    "kursawe": get_nsga2_toolbox,
    "zdt3": get_nsga2_toolbox,
    "zdt6": get_nsga2_toolbox,
    "frams": get_frams_nsga2_toolbox,
    "frams2": get_frams_nsga2_toolbox,
    "frams3": get_frams_nsga2_toolbox,
    "frams4": get_frams_nsga2_toolbox,
    "frams5": get_frams_one_criteria_toolbox,
    "h1": get_one_criteria_toolbox,
    "ackley": get_one_criteria_toolbox,
    "himmelblau": get_one_criteria_toolbox,
    "schwefel": get_one_criteria_toolbox,
    "rastrigin": get_one_criteria_toolbox
}


class Experiment:

    def __init__(self, experiment_name: str, **kwargs):
        self.toolbox = EXPERIMENTS[experiment_name](experiment_name, **kwargs)
