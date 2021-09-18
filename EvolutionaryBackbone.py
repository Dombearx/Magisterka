from typing import Callable
import pprint as pp
import numpy as np
import matplotlib.pyplot as plt
import time

from deap import base, tools
from HallOfFame import BasicParetoFront
from utils import save_results, serialize_experiment


class EvolutionaryBackbone:

    def __init__(self,
                 create_population: Callable[[base.Toolbox], list],
                 run_algorithm: Callable[[list, tools.Logbook, tools.Statistics, BasicParetoFront,
                                          Callable[[base.Toolbox, list, BasicParetoFront],
                                                   tuple[BasicParetoFront, int]]], tuple[list, list]],
                 migrate: Callable[[list], list],
                 should_still_run: Callable[[int, int], bool],
                 clear_results: Callable[[list], list],
                 prepare_hall_of_fame: Callable[[base.Toolbox], BasicParetoFront],
                 prepare_logs: Callable[[base.Toolbox], tuple[list, tools.Statistics]],
                 update_hall_of_fame: Callable[[base.Toolbox, list, BasicParetoFront], tuple[BasicParetoFront, int]],
                 print_statistics: Callable[[list, BasicParetoFront, int, ...], None],
                 toolbox: base.Toolbox,
                 iter_number: int,
                 experiment_name,
                 experiment_data,
                 key,
                 id,
                 name,
                 *args, **kwargs):
        self.toolbox = toolbox

        self.create_population = create_population
        self.run_algorithm = run_algorithm

        self.should_still_run = should_still_run
        self.clear_results = clear_results

        self.prepare_hall_of_fame = prepare_hall_of_fame
        self.update_hall_of_fame = update_hall_of_fame

        self.prepare_logs = prepare_logs

        self.print_statistics = print_statistics

        self.migrate = migrate

        self.iter_number = iter_number
        self.experiment_name = experiment_name
        self.experiment_data = experiment_data
        self.key = key
        self.id = id
        self.name = name

    def run(self) -> tuple[BasicParetoFront, list, list]:
        should_run = True

        populations = self.create_population(self.toolbox)

        hall_of_fame = self.prepare_hall_of_fame(self.toolbox)
        logs, stats = self.prepare_logs(self.toolbox)

        iteration_number = 0
        serialization_frequency = 5000

        other_data = []
        # TEST
        # plt.ion()
        # fig, ax = plt.subplots()
        # x, y = [], []
        # dots = ax.scatter(x, y, s=12)
        # plt.gca().set_aspect('equal', adjustable='box')
        # plt.xlim(0, 2)
        # plt.ylim(0, 2)
        #
        # plt.draw()
        # TEST
        dots = []
        fig = []
        iters = 0
        direction = self.toolbox.direction.keywords['direction']
        start_time = time.time()
        while should_run:
            other_data.append({"iteration_number": iteration_number, "number_of_islands": len(populations)})

            populations = self.migrate(populations, direction)

            index = [0, 1, 2, 3, 4]
            # hall_of_fame updates inplace
            t = time.time()
            result = self.toolbox.map(
                lambda population, log, i: self.run_algorithm(population, log, stats, hall_of_fame,
                                                              self.update_hall_of_fame, dots, fig, i), populations,
                logs, index)

            populations, logs, removed_individuals = self.clear_results(result)
            if removed_individuals > 0:
                iters = 0
            else:
                iters += 1

            print(
                f"{iters = } {iteration_number = } {hall_of_fame.get_best_individual_fitness()} {time.time() - t} {len(hall_of_fame.items)} {len(populations)}")

            # print(removed_individuals)

            # hall_of_fame, removed_individuals = self.update_hall_of_fame(self.toolbox, populations, hall_of_fame)

            self.print_statistics(populations, hall_of_fame, iteration_number, logs, removed_individuals)

            # pp.pp(hall_of_fame)
            # TEST
            # v = []
            #
            # for hofer in hall_of_fame:
            #     v.append(hofer.fitness.values)
            #
            # v = np.array(v)
            # # print(v[:5])
            # # print("-----")
            #
            # x = v[:, 0]
            # y = v[:, 1]
            # #
            # dots.set_offsets(np.c_[x, y])
            # fig.canvas.draw_idle()
            # plt.pause(0.1)

            # TEST

            iteration_number += 1

            if iteration_number % 100 == 0:
                save_results(self.experiment_name, self.experiment_name + "_snap_", self.iter_number, hall_of_fame,
                             logs, other_data, time.time() - start_time,
                             self.experiment_data)

            # if iteration_number % serialization_frequency == 0:
            #     filename = "experiment_" + str(self.id)
            #     serialize_experiment(filename, self.experiment_data, self.key, other_data, populations, logs,
            #                          should_run, hall_of_fame, iteration_number, self.iter_number, self.name, iters)

            should_run = self.should_still_run(removed_individuals, iteration_number)

        return hall_of_fame, logs, other_data

    def resolve_exp(self, exp):

        experiment_data = exp.experiment_data
        key = exp.key
        other_data = exp.other_data
        populations = exp.populations
        logs = exp.logs
        should_run = exp.should_run
        hall_of_fame = exp.hall_of_fame
        iteration_number = exp.iteration_number
        iter_number = exp.iter_number
        name = exp.name
        iters = exp.iters

        return experiment_data, key, other_data, populations, logs, should_run, hall_of_fame, iteration_number, iter_number, name, iters


    def run_from_file(self, exp) -> tuple[BasicParetoFront, list, list]:

        experiment_data, key, other_data, populations, logs, should_run, hall_of_fame, iteration_number, iter_number, name, iters = self.resolve_exp(exp)

        _, stats = self.prepare_logs(self.toolbox)
        self.iter_number = iter_number
        serialization_frequency = 5

        dots = []
        fig = []
        direction = self.toolbox.direction.keywords['direction']
        start_time = time.time()
        while should_run:
            other_data.append({"iteration_number": iteration_number, "number_of_islands": len(populations)})

            populations = self.migrate(populations, direction)

            index = [0, 1, 2, 3, 4]
            # hall_of_fame updates inplace
            t = time.time()
            result = self.toolbox.map(
                lambda population, log, i: self.run_algorithm(population, log, stats, hall_of_fame,
                                                              self.update_hall_of_fame, dots, fig, i), populations,
                logs, index)

            populations, logs, removed_individuals = self.clear_results(result)
            if removed_individuals > 0:
                iters = 0
            else:
                iters += 1

            print(
                f"{iters = } {iteration_number = } {hall_of_fame.get_best_individual_fitness()} {time.time() - t} {len(hall_of_fame.items)} {len(populations)}")

            self.print_statistics(populations, hall_of_fame, iteration_number, logs, removed_individuals)

            iteration_number += 1

            if iteration_number % 100 == 0:
                save_results(self.experiment_name, self.experiment_name + "_snap_", self.iter_number, hall_of_fame,
                             logs, other_data, time.time() - start_time,
                             self.experiment_data)

            if iteration_number % serialization_frequency == 0:
                filename = "experiment_" + str(self.id)
                serialize_experiment(filename, self.experiment_data, self.key, other_data, populations, logs,
                                     should_run, hall_of_fame, iteration_number, self.iter_number, name, iters)

            should_run = self.should_still_run(removed_individuals, iteration_number)

        return hall_of_fame, logs, other_data

# TODO
# Trzeba jeszcze zapisywać iters, bo inaczej wznawia tak jakby nie było progressu w ogóle. No i coś działa źle bo nei optymalizuje i przyszpiesza.