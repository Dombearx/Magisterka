import cProfile
import pstats
import time

from deap import tools

from AlgorithmBackboneInPlace import Nsga2Algorithm
from EvolutionaryBackbone import EvolutionaryBackbone
from HallOfFame import prepare_hall_of_fame, update_hall_of_fame, prepare_precision_hall_of_fame
from Logs import logs_do_nothing, update_logs, prepare_standard_logbook
from Migration import migrate_one_front_one_island, migrate_const_islands, migrate_random
from Populations import create_simple_population, create_islands_population, population_do_nothing
from Results import clear_do_nothing, clear_population
from ShouldRun import n_iters_run, n_iters_without_improvement
from Statistics import print_statistics
from experiments import Experiment
from utils import load_config, save_results

OPTIMIZATION_CRITERIA = ['velocity']

if __name__ == "__main__":

    config = load_config("experiment_conf.json")

    experiment_name = "frams"
    experiment_data = config["experiments"][experiment_name]
    experiment_args = experiment_data["experiment_args"]
    nsga2_args = experiment_data["nsga2_args"]
    main_alg_args = experiment_data["main_alg_args"]

    experiment = Experiment(experiment_name, **experiment_args)
    toolbox = experiment.toolbox

    alg = Nsga2Algorithm(
        toolbox,
        **nsga2_args
    )

    evolutionary_backbone = EvolutionaryBackbone(
        create_islands_population,
        population_do_nothing,
        alg.run,
        migrate_const_islands,
        n_iters_without_improvement,
        clear_population,
        prepare_precision_hall_of_fame,
        prepare_standard_logbook,
        update_hall_of_fame,
        update_logs,
        print_statistics,
        toolbox,
        **main_alg_args
    )

    start_time = time.time()

    with cProfile.Profile() as pr:
        hall_of_fame, logs = evolutionary_backbone.run()

    final_time = time.time() - start_time

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

    save_results(experiment_name, hall_of_fame, logs, final_time, experiment_data)
