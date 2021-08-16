#  benchmarks
from deap import creator, base, tools, benchmarks
import random

try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequenc

from framsticks.new_frams.FramsticksLib import FramsticksLib
from FramsWrapper import wrapper_evaluate, wrapper_mutate, \
    wrapper_crossover, wrapper_get_simplest, wrapper_crossover_one_child


def gaussian_mutation(individual, mu, sigma, index, upper_bound, lower_bound):
    val = individual[index]
    val += random.gauss(mu, sigma)
    val = max(min(val, upper_bound), lower_bound)
    return val


def random_mut_gaussian(ind, mu, sigma, upper_bound, lower_bound):
    index = random.randint(0, len(ind) - 1)

    return gaussian_mutation(ind, mu=mu, sigma=sigma, index=index, upper_bound=upper_bound, lower_bound=lower_bound)


# Wielokryterialne do NSGA2

BENCHMARKS = {
    "dtlz1": benchmarks.dtlz1,
    "dtlz2": benchmarks.dtlz2,
    "dtlz3": benchmarks.dtlz3,
    "dtlz4": benchmarks.dtlz4,
}


def get_frams_nsga2_toolbox(experiment_name, frams_path, optimization_criteria):
    creator.create("FitnessMax", base.Fitness, weights=[1.0] * len(optimization_criteria))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    attributes = 1

    cli = FramsticksLib(frams_path, None, None)

    toolbox = base.Toolbox()

    toolbox.register("attr_frams", wrapper_get_simplest, cli, '1')
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_frams, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", wrapper_evaluate, cli)
    toolbox.register("mate", wrapper_crossover, cli)
    toolbox.register("mutate", wrapper_mutate, cli)

    toolbox.register("select", tools.selNSGA2)

    return toolbox


def get_nsga2_toolbox(benchmark_name, direction: str, objectives, lower_bound, upper_bound, *args):
    if direction == "min":
        weights_tuple = (-1,) * objectives
    else:
        weights_tuple = (1,) * objectives

    creator.create("FitnessMin", base.Fitness, weights=weights_tuple)
    creator.create("Individual", list, fitness=creator.FitnessMin)

    attributes = objectives  # objectives + k - 1 ????????????

    toolbox = base.Toolbox()

    toolbox.register("attr_float", random.uniform, lower_bound, upper_bound)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval_benchmark(individual):
        return BENCHMARKS[benchmark_name](individual, objectives, *args)

    toolbox.register("evaluate", eval_benchmark)
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", random_mut_gaussian, mu=0,
                     sigma=(upper_bound - lower_bound) / 10, upper_bound=upper_bound, lower_bound=lower_bound)

    toolbox.register("select", tools.selNSGA2)

    toolbox.register("map", map)

    return toolbox
