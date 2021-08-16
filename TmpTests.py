import random

from deap import base

from Migration import sort_by_fitness
from Populations import create_simple_population
from experiments import Experiment

from framsticks.new_frams.FramsticksLib import FramsticksLib
counter = 0
def test_func():
    global counter
    counter += 1

    print(counter)



if __name__ == "__main__":

    test_func()

    test_func()
    test_func()
    test_func()

    # Not working: C(LLRX[|, p:0.25, r:1][|]X[|, p:0.1], )

    # genotype_list = ['C(LLRX[|, p:0.25, r:1][|]X[|, p:0.1], )']

    # genotype_list = ['C(LLRX[|, p:0.25, r:1][|]X[|, p:0.1], )']
    #
    # frams_path = r'H:\Polibuda\Magisterka\Magisterka\framsticks\Framsticks50rc19'
    # optimization_criteria = ['vertpos', 'velocity']
    #
    # cli = FramsticksLib(frams_path, None, None)
    #
    # results = cli.evaluate(genotype_list)
    #
    # print(results)
    # experiment = Experiment("dtlz1", 3)
    # toolbox = experiment.toolbox
    #
    # pop = create_simple_population(toolbox, 5)
    #
    # invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    # fitness_results = toolbox.map(toolbox.evaluate, invalid_ind)
    # for ind, fit in zip(invalid_ind, fitness_results):
    #     ind.fitness.values = fit
    #
    # for ind in pop:
    #     print(ind.fitness)
    #
    # pop = sort_by_fitness(pop)
    # print("---")
    # for ind in pop:
    #     print(ind.fitness)
