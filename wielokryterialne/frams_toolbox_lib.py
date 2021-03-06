#  benchmarks
from deap import creator, base, tools

from framsticks.new_frams.FramsticksLib import FramsticksLib


def register_standard(attributes, creator, cli):
    toolbox = base.Toolbox()

    toolbox.register("attr_frams", cli.getSimplest, '1')
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_frams, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", cli.evaluate)
    toolbox.register("mate", cli.crossOver)
    toolbox.register("mutate", cli.mutate)

    toolbox.register("select", tools.selNSGA2)

    return toolbox


def get_toolbox(experiment_name, frams_path, optimization_criteria):
    creator.create("FitnessMax", base.Fitness, weights=[1.0] * len(optimization_criteria))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    attributes = 1

    cli = FramsticksLib(frams_path, None, None)

    toolbox = register_standard(attributes, creator, cli)

    return toolbox
