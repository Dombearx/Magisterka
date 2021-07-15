import random

from deap import creator, base, tools, benchmarks
import pprint as pp

from experiments import Experiment
from Populations import create_simple_population, create_islands_population
from ClearPopulation import do_nothing
from HallOfFame import prepare_hall_of_fame

from EvolutionaryBackbone import EvolutionaryBackbone

OPTIMIZATION_CRITERIA = ['velocity']

if __name__ == "__main__":
    n_attributes = 2

    weights_tuple = (-1,) * n_attributes

    creator.create("FitnessMin", base.Fitness, weights=weights_tuple)
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    toolbox.register("attr_float", random.uniform, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_float, n_attributes)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    pop = create_simple_population(toolbox, 100)

    kwargs = {
        'create_population_args': None,
        'prepare_hall_of_fame_args': None,
        'should_still_run_args': None,
    }

    evolutionary_backbone = EvolutionaryBackbone(
        create_simple_population,
        do_nothing,

        toolbox
    )

    evolutionary_backbone.run()


    pp.pprint(pop)

    # print(f"Running {__name__}")
    #
    # e = Experiment("frams", "./framsticks/Framsticks50rc19", OPTIMIZATION_CRITERIA)
    #
    # print(e.toolbox)
