import cProfile
import pstats

from deap import tools

from AlgorithmBackbone import Nsga2Algorithm
from EvolutionaryBackbone import EvolutionaryBackbone
from HallOfFame import prepare_hall_of_fame, update_hall_of_fame
from Logs import logs_do_nothing, update_logs
from Migration import migrate_one_front_one_island, migrate_const_islands, migrate_random
from Populations import create_simple_population, create_islands_population, population_do_nothing, clear_do_nothing, clear_population
from ShouldRun import n_iters_run, NItersWithoutImprovement
from Statistics import print_statistics
from experiments import Experiment
from utils import load_config

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

    config = load_config("experiment_conf.json")

    experiments = config["experiments"]["dtlz1"]
    print(experiments)

    # experiment_name = experiments.keys()[0]

    objectives = 3
    lower_bound = 0.0
    upper_bound = 1.0
    # experiment = Experiment("dtlz2", objectives, lower_bound, upper_bound)
    frams_path = r'H:\Polibuda\Magisterka\Magisterka\framsticks\Framsticks50rc19'
    optimization_criteria = ['vertpos', 'velocity']
    experiment = Experiment("frams", frams_path, optimization_criteria)
    toolbox = experiment.toolbox

    mutation_probability = 0.9
    crossover_probability = 0.5
    number_of_generations = 100
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
        NItersWithoutImprovement().n_iters_without_improvement,
        clear_population,
        prepare_hall_of_fame,
        logs_do_nothing,
        update_hall_of_fame,
        update_logs,
        print_statistics,
        toolbox,
        create_population_args=[3, 2],
        prepare_hall_of_fame_args=[10],
        should_still_run_args=[100],
        migrate_args=[2]
    )

    with cProfile.Profile() as pr:
        hall_of_fame, logs = evolutionary_backbone.run()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

    for ind in hall_of_fame:
        print(ind, ind.fitness)

    # pp.pprint(pop)

    # print(f"Running {__name__}")
    #
    # e = Experiment("frams", "./framsticks/Framsticks50rc19", OPTIMIZATION_CRITERIA)
    #
    # print(e.toolbox)
