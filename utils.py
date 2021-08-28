import json
from HallOfFame import BasicParetoFront
import pickle
from datetime import datetime


def load_config(filename: str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)

    return data


def defer(fn, args1):
    def run(*args2):
        return fn(*args2, **args1)

    return run


class Result:

    def __init__(self, logbooks, hall_of_fame, time, experiment_args):
        self.logbooks = logbooks
        self.hall_of_fame = hall_of_fame
        self.time = time
        self.experiment_args = experiment_args

    def get_logbooks(self):
        return self.logbooks

    def get_hall_of_fame(self):
        return self.hall_of_fame

    def get_time(self):
        return self.time

    def get_experiment_args(self):
        return self.experiment_args


def save_results(experiment_name: str, hall_of_fame: BasicParetoFront, logs: list, time: float,
                 experiment_args: dict) -> None:
    time_text = datetime.now().strftime("%Y-%m-%d_%H-%M")
    print(time_text)

    pickleOut = open("./Tests_results/" + experiment_name + "_" + time_text + ".pickle", "wb")

    pickle.dump(Result(logs, hall_of_fame, time, experiment_args), pickleOut)

    pickleOut.close()
