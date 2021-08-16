import json
from HallOfFame import BasicParetoFront
import pickle


def load_config(filename: str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)

    return data


class Result:

    def __init__(self, logbooks, hall_of_fame, time):
        self.logbooks = logbooks
        self.hall_of_fame = hall_of_fame
        self.time = time

    def get_logbooks(self):
        return self.logbooks

    def get_hall_of_fame(self):
        return self.hall_of_fame

    def get_time(self):
        return self.time


def save_results(benchmark_name: str, benchmark_stats, hall_of_fame: BasicParetoFront, logs: list, time: float) -> None:
    pickleOut = open("./Tests_results/" + benchmark_name + "_" + "_".join(*benchmark_stats) + ".pickle", "wb")

    pickle.dump(Result(logs, hall_of_fame, time), pickleOut)

    pickleOut.close()
