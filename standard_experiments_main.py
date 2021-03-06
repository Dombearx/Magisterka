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

def resume_one_experiment(config, name, id, key, iter_number, pickle_path):
    standard_data = ["algorithm_args", "toolbox"]
    prefix = "main_alg_args_"

    experiment_data = config["experiments"]["multi_criteria"]
    experiment_args = config["experiments_params"][name]["experiment_args"]
    algorithm_args = experiment_data["algorithm_args"]
    algorithm_args2 = config["experiments_params"][name]["algorithm_args"]

    toolbox_name = name
    main_alg_args = experiment_data[key]

    experiment_name = name + "_" + key[key.find(prefix) + len(prefix):]

    experiment = Experiment(toolbox_name, **experiment_args)
    toolbox = experiment.toolbox

    exp = deserialize_experiment(pickle_path)

    alg = getattr(AlgorithmBackboneInPlace, algorithm_args["name"])(
        toolbox,
        **algorithm_args["args"],
        **algorithm_args2
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

    hall_of_fame, other_data = evolutionary_backbone.run_from_file(exp)

    final_time = time.time() - start_time

    print(experiment_name, hall_of_fame[0].fitness, hall_of_fame)
    save_results(experiment_name, experiment_name, iter_number, hall_of_fame, other_data, final_time,
                 experiment_data)

def make_one_experiment(config, name, id, key, iter_number):
    standard_data = ["algorithm_args", "toolbox"]
    prefix = "main_alg_args_"

    experiment_data = config["experiments"]["multi_criteria"]
    experiment_args = config["experiments_params"][name]["experiment_args"]
    algorithm_args = experiment_data["algorithm_args"]
    algorithm_args2 = config["experiments_params"][name]["algorithm_args"]

    toolbox_name = name

    print("current:", key)
    main_alg_args = experiment_data[key]

    experiment_name = name + "_" + key[key.find(prefix) + len(prefix):]

    experiment = Experiment(toolbox_name, **experiment_args)
    toolbox = experiment.toolbox

    alg = getattr(AlgorithmBackboneInPlace, algorithm_args["name"])(
        toolbox,
        **algorithm_args["args"],
        **algorithm_args2
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
    hall_of_fame, other_data = evolutionary_backbone.run()

    final_time = time.time() - start_time

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # # stats.print_stats()

    print(experiment_name, hall_of_fame[0].fitness, hall_of_fame)
    save_results(experiment_name, experiment_name, iter_number, hall_of_fame, other_data, final_time,
                 experiment_data)


if __name__ == "__main__":

    folder_path = "./" + "pickles"
    done_folder_path = "./" + "dones"
    json_file = "multi_config.json"

    if len(sys.argv) == 4:
        iter_number = int(sys.argv[1])
        name = sys.argv[2]
        key = sys.argv[3]
    else:
        iter_number = 0
        name = "dtlz1"
        key = "main_alg_args_convection_selection_front_islands"

    cfg = load_config(json_file)

    id = str(iter_number) + "_" + name + "_" + key

    if os.path.exists(done_folder_path + "/" + "experiment_" + str(id) + "_done.txt"):
        print("EXPERIMENT ALREADY DONE")
    else:
        if os.path.exists(folder_path + "/" + "experiment_" + str(id) + ".pickle"):
            resume_one_experiment(cfg, name, id, key, iter_number, "experiment_" + id)
        else:
            make_one_experiment(cfg, name, id, key, iter_number)
