from wielokryterialne.benchmarks_conf import get_dtlz1_toolbox, getDTLZ2ToolBox, getDTLZ3ToolBox, getDTLZ4ToolBox
from wielokryterialne.frams_toolbox_lib import get_toolbox

EXPERIMENTS = {
    "dtlz1": get_dtlz1_toolbox,
    "dtlz2": getDTLZ2ToolBox,
    "dtlz3": getDTLZ3ToolBox,
    "dtlz4": getDTLZ4ToolBox,
    "frams": get_toolbox
}


class Experiment:

    def __init__(self, experiment_name: str, *args):

        self.toolbox = EXPERIMENTS[experiment_name](*args)

