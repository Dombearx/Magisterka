import cProfile
import pstats
import time
import sys
import os

from deap import tools

import AlgorithmBackboneInPlace
from EvolutionaryBackbone import EvolutionaryBackbone
import HallOfFame
import Logs
import Populations
import Migration
import ShouldRun
import Results
import Statistics
from experiments import Experiment
from utils import load_config, save_results, defer, deserialize_experiment


def resolve_config_entry(module, config_entry):
    return defer(getattr(module, config_entry["name"]), config_entry["args"])


def make_one_experiment(config, name, iter_number, number_of_criteria, id):
    standard_data = ["algorithm_args", "toolbox"]
    prefix = "main_alg_args_"

    experiment_data = config["experiments"][number_of_criteria]
    experiment_args = config["experiments_params"][name]["experiment_args"]
    algorithm_args = experiment_data["algorithm_args"]

    keys = [key for key in experiment_data.keys() if key not in standard_data]

    # keys = ["main_alg_args_standard", ]

    toolbox_name = name
    for key in keys:
        print("current:", key)
        main_alg_args = experiment_data[key]

        experiment_name = name + "_" + key[key.find(prefix) + len(prefix):]

        experiment = Experiment(toolbox_name, **experiment_args)
        toolbox = experiment.toolbox

        alg = getattr(AlgorithmBackboneInPlace, algorithm_args["name"])(
            toolbox,
            **algorithm_args["args"]
        )

        evolutionary_backbone = EvolutionaryBackbone(
            resolve_config_entry(Populations, main_alg_args["create_population"]),
            alg.run,
            resolve_config_entry(Migration, main_alg_args["migrate"]),
            resolve_config_entry(ShouldRun, main_alg_args["should_run"]),
            resolve_config_entry(Results, main_alg_args["get_results"]),
            resolve_config_entry(HallOfFame, main_alg_args["prepare_hall_of_fame"]),
            resolve_config_entry(Logs, main_alg_args["prepare_logbook"]),
            resolve_config_entry(HallOfFame, main_alg_args["update_hall_of_fame"]),
            resolve_config_entry(Statistics, main_alg_args["print_statistics"]),
            toolbox,
            iter_number,
            experiment_name,
            experiment_data,
            key,
            id,
            name
        )

        start_time = time.time()

        # with cProfile.Profile() as pr:
        hall_of_fame, logs, other_data = evolutionary_backbone.run()

        final_time = time.time() - start_time

        # stats = pstats.Stats(pr)
        # stats.sort_stats(pstats.SortKey.TIME)
        # stats.print_stats()

        print(experiment_name, hall_of_fame[0].fitness, hall_of_fame)
        save_results(experiment_name, experiment_name, iter_number, hall_of_fame, logs, other_data, final_time,
                     experiment_data)


def main(config, iter_number, number_of_criteria, name2, id):
    names = config["experiments"][number_of_criteria]["toolbox"]

    for name in names:
        print("Current:", iter_number, name, id)
        make_one_experiment(config, name, iter_number, number_of_criteria, id)


if __name__ == "__main__":

    cfg = load_config("frams_config.json")

    all_names = cfg["experiments"].keys()
    number_of_tests = 6
    if len(sys.argv) == 4:
        start = int(sys.argv[1])
        stop = int(sys.argv[2])
        name = sys.argv[2]
    else:
        start = 0
        stop = 1
        name = "h1"

    # number_of_criteria = "one_criteria"
    number_of_criteria = "multi_criteria"

    id = 1237891237

    folder_path = "./" + "pickles"

    for i in range(start, stop):
        main(cfg, i, number_of_criteria, name, id)
