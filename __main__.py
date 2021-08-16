import cProfile
import pstats
import time

from deap import tools

from AlgorithmBackbone import Nsga2Algorithm
from EvolutionaryBackbone import EvolutionaryBackbone
from HallOfFame import prepare_hall_of_fame, update_hall_of_fame, prepare_precision_hall_of_fame
from Logs import logs_do_nothing, update_logs, prepare_standard_logbook
from Migration import migrate_one_front_one_island, migrate_const_islands, migrate_random
from Populations import create_simple_population, create_islands_population, population_do_nothing
from Results import clear_do_nothing, clear_population
from ShouldRun import n_iters_run, NItersWithoutImprovement
from Statistics import print_statistics
from experiments import Experiment
from utils import load_config, save_results

OPTIMIZATION_CRITERIA = ['velocity']

if __name__ == "__main__":
    # n_attributes = 2
    #
    # weights_tuple = (-1,) * n_attributes
    #
    # creator.create("FitnessMin", base.Fitness, weights=weights_tuple)
    # creator.create("Individual", list, fitness=creator.FitnessMin)
    #
    # toolbox = base.Toolbox()
    #
    # toolbox.register("attr_float", random.uniform, 0, 1)
    # toolbox.register("individual", tools.initRepeat, creator.Individual,
    #                  toolbox.attr_float, n_attributes)
    # toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # TODO Make config work as it should
    config = load_config("experiment_conf.json")

    experiments = config["experiments"]["dtlz1"]
    print(experiments)

    # experiment_name = experiments.keys()[0]

    objectives = 3
    lower_bound = 0.0
    upper_bound = 1.0
    # TODO Fix gaussian mutation
    # experiment = Experiment("dtlz2", objectives, lower_bound, upper_bound)
    frams_path = r'H:\Polibuda\Magisterka\Magisterka\framsticks\Framsticks50rc19'
    optimization_criteria = ['vertpos', 'velocity']
    experiment = Experiment("frams", frams_path, optimization_criteria)
    toolbox = experiment.toolbox

    mutation_probability = 0.9
    crossover_probability = 0.5
    number_of_generations = 5
    sort_population = tools.selTournamentDCD

    alg = Nsga2Algorithm(
        toolbox,
        mutation_probability,
        crossover_probability,
        number_of_generations,
        sort_population,
        optimization_criteria=optimization_criteria
    )

    pop = create_simple_population(toolbox, 3)

    evolutionary_backbone = EvolutionaryBackbone(
        create_islands_population,
        population_do_nothing,
        alg.run,
        migrate_const_islands,
        # n_iters_run,
        NItersWithoutImprovement().n_iters_without_improvement,
        clear_population,
        prepare_precision_hall_of_fame,
        prepare_standard_logbook,
        update_hall_of_fame,
        update_logs,
        print_statistics,
        toolbox,
        create_population_args=[2, 4],
        prepare_hall_of_fame_args=[10, [2, 2]],
        should_still_run_args=[2],
        migrate_args=[2],
        create_logs_args=[2]
    )

    start_time = time.time()

    with cProfile.Profile() as pr:
        hall_of_fame, logs = evolutionary_backbone.run()

    final_time = time.time() - start_time

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

    for ind in hall_of_fame:
        print(ind, ind.fitness)

    # TODO Saving results (just name for file needed)
    # save_results(hall_of_fame, logs, final_time)


    # pp.pprint(pop)

    # print(f"Running {__name__}")
    #
    # e = Experiment("frams", "./framsticks/Framsticks50rc19", OPTIMIZATION_CRITERIA)
    #
    # print(e.toolbox)
