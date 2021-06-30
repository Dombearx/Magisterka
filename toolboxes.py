from deap import creator, base, tools, benchmarks
import random

def changedMutGaussian(individual, mu, sigma, index, upper_bound, lower_bound):
    individual[index] += random.gauss(mu, sigma)
    individual[index] = max(min(individual[index], upper_bound), lower_bound)
    return individual,


def random_gaussian_mutation(ind, mu, sigma, upper_bound, lower_bound):
    index = random.randint(0, len(ind)-1)

    return changedMutGaussian(ind, mu=mu, sigma=sigma, index=index, upper_bound=upper_bound, lower_bound=lower_bound)

def register_NSGA2(lower_bound, upper_bound, attributes, creator, evalBenchmark):

    toolbox = base.Toolbox()

    toolbox.register("attr_float", random.uniform, lower_bound, upper_bound)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalBenchmark)
    toolbox.register("mate", tools.cxUniform, indpb=0.5)
    toolbox.register("mutate", random_gaussian_mutation, mu=0,
                     sigma=(upper_bound - lower_bound)/10, upper_bound=upper_bound, lower_bound=lower_bound)

    toolbox.register("select", tools.selNSGA2)

    return toolbox

def get_toolbox(experiment_name: str, **kwargs):

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


def get_toolbox(frams_path, OPTIMIZATION_CRITERIA):
    creator.create("FitnessMax", base.Fitness, weights=[1.0] * len(OPTIMIZATION_CRITERIA))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    attributes = 1

    cli = FramsticksLib(frams_path, None, None)

    toolbox = register_standard(attributes, creator, cli)

    return toolbox