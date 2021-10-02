import json
from HallOfFame import BasicParetoFront
import pickle
from datetime import datetime
import os
from deap import tools
import numpy as np

def load_config(filename: str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)

    return data


def defer(fn, args1):
    def run(*args2):
        return fn(*args2, **args1)

    return run

def calculate_best_value(hall_of_fame):
    if len(hall_of_fame[0].fitness.values) == 1:
        # one criteria
        best_value = hall_of_fame[0].fitness.values
    else:
        # multi criteria
        all_points = []
        for hofer in hall_of_fame:
            all_points.append([i for i in hofer.fitness.values])

        ref_point = np.array(all_points).max(axis=0)
        ref_point = (-10, 30)

        best_value = tools.hypervolume(hall_of_fame, ref=ref_point)

    return best_value

class Serialized_experiment:

    def __init__(self, experiment_data, key, other_data, populations, should_run, hall_of_fame,
                 iteration_number, iter_number, name, iters, old_time):
        self.experiment_data = experiment_data
        self.key = key
        self.other_data = other_data
        self.populations = populations
        # self.logs = logs
        self.should_run = should_run
        self.hall_of_fame = hall_of_fame
        self.iteration_number = iteration_number
        self.iter_number = iter_number
        self.name = name
        self.iters = iters
        self.old_time = old_time


def serialize_experiment(filename, experiment_data, key, other_data, populations, should_run, hall_of_fame,
                         iteration_number, iter_number, name, iters, old_time):
    # stats = ""

    exp = Serialized_experiment(experiment_data, key, other_data, populations, should_run, hall_of_fame,
                                iteration_number, iter_number, name, iters, old_time)

    folder_path = "./" + "pickles"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    pickleOut = open(folder_path + "/" + filename + ".pickle", "wb")
    pickle.dump(exp, pickleOut)
    pickleOut.close()


def deserialize_experiment(filename):
    folder_path = "./" + "pickles"

    with (open(folder_path + "/" + filename + ".pickle", "rb")) as openfile:
        exp = pickle.load(openfile)

    return exp


def create_done_file(filename):
    folder_path = "./" + "dones"

    with(open(folder_path + "/" + filename + "_done.txt", "w")) as f:
        f.write("DONE")


class Result:

    def __init__(self, hall_of_fame, time, experiment_args, other_data):
        # self.logbooks = logbooks
        self.hall_of_fame = hall_of_fame
        self.time = time
        self.experiment_args = experiment_args
        self.other_data = other_data

    # def get_logbooks(self):
    #     return self.logbooks

    def get_hall_of_fame(self):
        return self.hall_of_fame

    def get_time(self):
        return self.time

    def get_experiment_args(self):
        return self.experiment_args

    def get_other_data(self):
        return self.other_data


def save_results(category_name: str, experiment_name: str, iter_number: int, hall_of_fame: BasicParetoFront, other_data: list, time: float,
                 experiment_args: dict) -> None:
    time_text = datetime.now().strftime("%Y-%m-%d_%H-%M")
    print(time_text)

    folder_path = "./Tests_results/" + category_name

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    pickleOut = open(folder_path + "/" + experiment_name + "_" + str(iter_number) + "_" + time_text + ".pickle", "wb")

    pickle.dump(Result(hall_of_fame, time, experiment_args, other_data), pickleOut)

    pickleOut.close()
