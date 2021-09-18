#  benchmarks
from deap import creator, base, tools, benchmarks
import random
import math

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
    individual[index] = val
    return individual


def random_mut_gaussian(ind, mu, sigma, upper_bound, lower_bound):
    index = random.randint(0, len(ind) - 1)

    return gaussian_mutation(ind, mu=mu, sigma=sigma, index=index, upper_bound=upper_bound, lower_bound=lower_bound)


def random_mut_all_gaussian(ind, attributes, mu, sigma, upper_bound, lower_bound):
    sigma = sigma / math.sqrt(attributes)
    for index in range(len(ind)):
        val = ind[index]
        val += random.gauss(mu, sigma)
        val = max(min(val, upper_bound), lower_bound)
        ind[index] = val

    return ind


def cx_uniform_one_child(ind1, ind2, indpb):
    i1, i2 = tools.cxUniform(ind1, ind2, indpb)

    return i1


BENCHMARKS = {
    "dtlz1": benchmarks.dtlz1,
    "dtlz2": benchmarks.dtlz2,
    "dtlz3": benchmarks.dtlz3,
    "dtlz4": benchmarks.dtlz4,
    "kursawe": benchmarks.kursawe,
    "zdt3": benchmarks.zdt3,
    "zdt6": benchmarks.zdt6,
    "h1": benchmarks.h1,
    "ackley": benchmarks.ackley,
    "himmelblau": benchmarks.himmelblau,
    "schwefel": benchmarks.schwefel,
    "rastrigin": benchmarks.rastrigin
}


def get_frams_nsga2_toolbox(experiment_name, frams_path, optimization_criteria, direction, sim_file):
    creator.create("Fitness", base.Fitness, weights=[1.0] * len(optimization_criteria))
    creator.create("ParetoFrontNumber", int)
    creator.create("Individual", list, fitness=creator.Fitness, front_number=creator.ParetoFrontNumber)

    attributes = 1

    cli = FramsticksLib(frams_path, None, sim_file)

    toolbox = base.Toolbox()

    toolbox.register("direction", str, direction=direction)

    toolbox.register("attr_frams", wrapper_get_simplest, cli, '1')
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_frams, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", wrapper_evaluate, cli)
    toolbox.register("mate", wrapper_crossover_one_child, cli)
    toolbox.register("mutate", wrapper_mutate, cli)

    toolbox.register("select", tools.selNSGA2)

    return toolbox


# TODO Inside crossover probability is hardcoded
def get_nsga2_toolbox(benchmark_name, direction: str, obj, lower_bound, upper_bound, **kwargs):
    if direction == "min":
        weights_tuple = (-1,) * 2
    else:
        weights_tuple = (1,) * 2

    creator.create("Fitness", base.Fitness, weights=weights_tuple)
    creator.create("ParetoFrontNumber", int)
    creator.create("Individual", list, fitness=creator.Fitness, front_number=creator.ParetoFrontNumber)

    attributes = obj  # objectives + k - 1 ????????????

    toolbox = base.Toolbox()

    toolbox.register("direction", str, direction=direction)

    toolbox.register("attr_float", random.uniform, lower_bound, upper_bound)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def eval_benchmark(individual):
        return BENCHMARKS[benchmark_name](individual, **kwargs)

    toolbox.register("evaluate", eval_benchmark)
    toolbox.register("mate", cx_uniform_one_child, indpb=0.5)
    toolbox.register("mutate", random_mut_all_gaussian, attributes=attributes, mu=0,
                     sigma=(upper_bound - lower_bound) / 100, upper_bound=upper_bound, lower_bound=lower_bound)

    toolbox.register("select", tools.selNSGA2)

    toolbox.register("map", map)

    return toolbox


def get_one_criteria_toolbox(benchmark_name, direction: str, attributes, lower_bound, upper_bound, *args):
    if direction == "min":
        weights_tuple = (-1.0,)
    else:
        weights_tuple = (1.0,)

    creator.create("Fitness", base.Fitness, weights=weights_tuple)
    creator.create("Individual", list, fitness=creator.Fitness)

    def eval_benchmark(individual):
        return BENCHMARKS[benchmark_name](individual, *args)

    toolbox = base.Toolbox()

    toolbox.register("direction", str, direction=direction)
    toolbox.register("attr_float", random.uniform, lower_bound, upper_bound)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", eval_benchmark)
    toolbox.register("mate", cx_uniform_one_child, indpb=0.5)
    toolbox.register("mutate", random_mut_all_gaussian, attributes=attributes, mu=0,
                     sigma=(upper_bound - lower_bound) / 100, upper_bound=upper_bound, lower_bound=lower_bound)

    # toolbox.register("mutate", random_mut_gaussian, mu=0,
    #                  sigma=0.2, upper_bound=upper_bound, lower_bound=lower_bound)

    toolbox.register("select", tools.selTournament, tournsize=3)

    toolbox.register("map", map)

    return toolbox
