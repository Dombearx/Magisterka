import cProfile
import pstats
import time
import sys
import os
import pickle

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


def make_one_experiment(config, name, id, key, iter_number, num_of_criteria, experiment_id=None):
    prefix = "main_alg_args_"

    experiment_data = config["experiments"][num_of_criteria]
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

    # with cProfile.Profile() as pr:
    exp = None
    if experiment_id:
        exp = deserialize_experiment(experiment_id)
    hall_of_fame, other_data, cumulative_time = evolutionary_backbone.run(verbose=True, exp=exp)

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

    print(experiment_name, "Done")
    save_results(experiment_name, experiment_name, iter_number, hall_of_fame, other_data, cumulative_time,
                 experiment_data)


if __name__ == "__main__":
    print("MAIN STARTS")

    folder_path = "./" + "pickles"
    done_folder_path = "./" + "dones"

    runner_config = load_config("runner.json")

    if len(sys.argv) == 2:
        runner_number = sys.argv[1]
    else:
        runner_number = '0'

    json_file = runner_config[runner_number]["json_file"]
    iter_min = runner_config[runner_number]["range_min"]
    iter_max = runner_config[runner_number]["range_max"]
    name = runner_config[runner_number]["toolbox_name"]
    num_of_criteria = runner_config[runner_number]["number_of_criteria"]

    print("CONFIG LOADING")
    cfg = load_config(json_file)

    for iter_number in range(iter_min, iter_max):
        for key in runner_config[runner_number]["keys"]:
            id = str(iter_number) + "_" + name + "_" + key

            print("SEARCHING FOR", folder_path + "/" + "experiment_" + str(id) + ".pickle")
            if os.path.exists(done_folder_path + "/" + "experiment_" + str(id) + "_done.txt"):
                print("EXPERIMENT ALREADY DONE")
            else:
                if os.path.exists(folder_path + "/" + "experiment_" + str(id) + ".pickle"):
                    try:
                        print("RESUMING", "experiment_" + id)
                        make_one_experiment(cfg, name, id, key, iter_number, num_of_criteria, "experiment_" + id)
                    except pickle.UnpicklingError:
                        print("PICKLE ERRIR RUNNING", "experiment_" + id)
                        make_one_experiment(cfg, name, id, key, iter_number, num_of_criteria)

                else:
                    print("RUNNING", "experiment_" + id)
                    make_one_experiment(cfg, name, id, key, iter_number, num_of_criteria)
