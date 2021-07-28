from deap import tools

from experiments import Experiment
from Populations import create_simple_population, create_islands_population, population_do_nothing, clear_do_nothing
from AlgorithmBackbone import Nsga2Algorithm
from ShouldRun import n_iters_run
from HallOfFame import prepare_hall_of_fame, update_hall_of_fame
from Logs import logs_do_nothing, update_logs
from utils import load_config
from EvolutionaryBackbone import EvolutionaryBackbone
from Statistics import print_statistics

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

    experiments = config["experiments"]
    print(experiments)

    # experiment_name = experiments.keys()[0]

    experiment = Experiment("dtlz1", 3)
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
        sort_population
    )

    pop = create_simple_population(toolbox, 100)

    evolutionary_backbone = EvolutionaryBackbone(
        create_simple_population,
        population_do_nothing,
        alg.run,
        n_iters_run,
        clear_do_nothing,
        prepare_hall_of_fame,
        logs_do_nothing,
        update_hall_of_fame,
        update_logs,
        print_statistics,
        toolbox,
        create_population_args=[100],
        prepare_hall_of_fame_args=[10],
        should_still_run_args=[5],
    )

    hall_of_fame, logs = evolutionary_backbone.run()

    for ind in hall_of_fame:
        print(ind, ind.fitness)

    # pp.pprint(pop)

    # print(f"Running {__name__}")
    #
    # e = Experiment("frams", "./framsticks/Framsticks50rc19", OPTIMIZATION_CRITERIA)
    #
    # print(e.toolbox)
