from wielokryterialne.benchmarks_conf import get_dtlz1_toolbox, get_dtlz2_toolbox, get_dtlz3_toolbox, get_dtlz4_toolbox
from wielokryterialne.frams_toolbox_lib import get_toolbox

EXPERIMENTS = {
    "dtlz1": get_dtlz1_toolbox,
    "dtlz2": get_dtlz2_toolbox,
    "dtlz3": get_dtlz3_toolbox,
    "dtlz4": get_dtlz4_toolbox,
    "frams": get_toolbox
}


class Experiment:

    def __init__(self, experiment_name: str, *args):

        self.toolbox = EXPERIMENTS[experiment_name](*args)

