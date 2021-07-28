#  benchmarks
from deap import creator, base, tools, benchmarks
import random

try:
    from collections.abc import Sequence
except ImportError:
    from collections import Sequenc


def changedMutGaussian(individual, mu, sigma, index, upper_bound, lower_bound):
    individual[index] += random.gauss(mu, sigma)
    individual[index] = max(min(individual[index], upper_bound), lower_bound)
    return individual,


def randomMutGaussian(ind, mu, sigma, upper_bound, lower_bound):
    index = random.randint(0, len(ind)-1)

    return changedMutGaussian(ind, mu=mu, sigma=sigma, index=index, upper_bound=upper_bound, lower_bound=lower_bound)


# Wielokryterialne do NSGA2


def register_NSGA2(lower_bound, upper_bound, attributes, creator, evalBenchmark):

    toolbox = base.Toolbox()

    toolbox.register("attr_float", random.uniform, lower_bound, upper_bound)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalBenchmark)
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", randomMutGaussian, mu=0,
                     sigma=(upper_bound - lower_bound)/10, upper_bound=upper_bound, lower_bound=lower_bound)

    toolbox.register("select", tools.selNSGA2)

    return toolbox


def get_dtlz1_toolbox(objectives):

    weights_tuple = (-1,) * objectives

    creator.create("FitnessMin", base.Fitness, weights=weights_tuple)
    creator.create("Individual", list, fitness=creator.FitnessMin)

    attributes = objectives  # objectives + k - 1 ????????????
    lower_bound = 0.0
    upper_bound = 1.0

    def eval_benchmark(individual):
        return benchmarks.dtlz1(individual, objectives)

    toolbox = register_NSGA2(
        lower_bound, upper_bound, attributes, creator, eval_benchmark)

    return toolbox


def get_dtlz2_toolbox(objectives):

    weights_tuple = (-1,) * objectives

    creator.create("FitnessMin", base.Fitness, weights=weights_tuple)
    creator.create("Individual", list, fitness=creator.FitnessMin)

    attributes = objectives  # objectives + k - 1 ????????????
    lower_bound = 0.0
    upper_bound = 1.0

    def evalBenchmark(individual):
        return benchmarks.dtlz2(individual, objectives)

    toolbox = register_NSGA2(
        lower_bound, upper_bound, attributes, creator, evalBenchmark)

    return toolbox


def get_dtlz3_toolbox(objectives):

    weights_tuple = (-1,) * objectives

    creator.create("FitnessMin", base.Fitness, weights=weights_tuple)
    creator.create("Individual", list, fitness=creator.FitnessMin)

    attributes = objectives  # objectives + k - 1 ????????????
    lower_bound = 0.0
    upper_bound = 1.0

    def evalBenchmark(individual):
        return benchmarks.dtlz3(individual, objectives)

    toolbox = register_NSGA2(
        lower_bound, upper_bound, attributes, creator, evalBenchmark)

    return toolbox


def get_dtlz4_toolbox(objectives):

    weights_tuple = (-1,) * objectives

    creator.create("FitnessMin", base.Fitness, weights=weights_tuple)
    creator.create("Individual", list, fitness=creator.FitnessMin)

    attributes = objectives  # objectives + k - 1 ????????????
    lower_bound = 0.0
    upper_bound = 1.0

    def evalBenchmark(individual):
        return benchmarks.dtlz4(individual, objectives, 100)

    toolbox = register_NSGA2(
        lower_bound, upper_bound, attributes, creator, evalBenchmark)

    return toolbox
