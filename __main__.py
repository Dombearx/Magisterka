import cProfile
import pstats
import time

from deap import tools

from AlgorithmBackboneInPlace import Nsga2Algorithm
from EvolutionaryBackbone import EvolutionaryBackbone
import HallOfFame
import Logs
import Populations
import Migration
import ShouldRun
import Results
import Statistics
from experiments import Experiment
from utils import load_config, save_results, defer

if __name__ == "__main__":

    config = load_config("experiment_conf.json")

    experiment_name = "dtlz1"
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

    create_population = main_alg_args["create_population"]
    migrate = main_alg_args["migrate"]
    should_run = main_alg_args["should_run"]
    get_results = main_alg_args["get_results"]
    prepare_hall_of_fame = main_alg_args["prepare_hall_of_fame"]
    prepare_logbook = main_alg_args["prepare_logbook"]
    update_hall_of_fame = main_alg_args["update_hall_of_fame"]
    update_logs = main_alg_args["update_logs"]
    print_statistics = main_alg_args["print_statistics"]

    print(Migration)

    evolutionary_backbone = EvolutionaryBackbone(
        defer(getattr(Populations, create_population["name"]), create_population["args"]),
        alg.run,
        defer(getattr(Migration, migrate["name"]), migrate["args"]),
        defer(getattr(ShouldRun, should_run["name"]), should_run["args"]),
        defer(getattr(Results, get_results["name"]), get_results["args"]),
        defer(getattr(HallOfFame, prepare_hall_of_fame["name"]), prepare_hall_of_fame["args"]),
        defer(getattr(Logs, prepare_logbook["name"]), prepare_logbook["args"]),
        defer(getattr(HallOfFame, update_hall_of_fame["name"]), update_hall_of_fame["args"]),
        defer(getattr(Logs, update_logs["name"]), update_logs["args"]),
        defer(getattr(Statistics, print_statistics["name"]), print_statistics["args"]),
        toolbox
    )

    start_time = time.time()

    with cProfile.Profile() as pr:
        hall_of_fame, logs = evolutionary_backbone.run()

    final_time = time.time() - start_time

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

    save_results(experiment_name, hall_of_fame, logs, final_time, experiment_data)
