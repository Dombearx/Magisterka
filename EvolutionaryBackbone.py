from typing import Callable
import pprint as pp
import numpy as np
import time

from deap import base, tools
from HallOfFame import BasicParetoFront
from utils import save_results, serialize_experiment, create_done_file, calculate_best_value


class EvolutionaryBackbone:

    def __init__(self,
                 create_population: Callable[[base.Toolbox], list],
                 run_algorithm: Callable[[list, tools.Logbook, tools.Statistics, BasicParetoFront,
                                          Callable[[base.Toolbox, list, BasicParetoFront],
                                                   tuple[BasicParetoFront, int]]], tuple[list, list]],
                 migrate: Callable[[list, str], list],
                 should_still_run: Callable[[int, int, int], bool],
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

    def resolve_exp(self, exp):

        experiment_data = exp.experiment_data
        key = exp.key
        other_data = exp.other_data
        populations = exp.populations
        should_run = exp.should_run
        hall_of_fame = exp.hall_of_fame
        iteration_number = exp.iteration_number
        iter_number = exp.iter_number
        name = exp.name
        iters = exp.iters

        return experiment_data, key, other_data, populations, should_run, hall_of_fame, iteration_number, iter_number, name, iters

    def prepare_run(self):
        should_run = True
        populations = self.create_population(self.toolbox)
        hall_of_fame = self.prepare_hall_of_fame(self.toolbox)
        iteration_number = 0
        other_data = []
        unchanged_iterations = 0
        return should_run, populations, hall_of_fame, iteration_number, other_data, unchanged_iterations

    def run(self, verbose=False, exp=None) -> tuple[BasicParetoFront, list]:
        if exp:
            self.experiment_data, self.key, other_collected_data, islands, should_run, hall_of_fame, iteration_number, self.iter_number, self.name, unchanged_iterations = self.resolve_exp(
                exp)
        else:
            should_run, islands, hall_of_fame, iteration_number, other_collected_data, unchanged_iterations = self.prepare_run()

        serialization_frequency = 5
        direction = self.toolbox.direction.keywords['direction']
        start_time = time.time()

        while should_run:
            print("Runned")
            islands = self.migrate(islands, direction)

            migration_time_start = time.time()

            result = self.toolbox.map(
                lambda island: self.run_algorithm(island, hall_of_fame, self.update_hall_of_fame), islands)

            islands, removed_individuals = self.clear_results(result)
            if removed_individuals > 0:
                unchanged_iterations = 0
            else:
                unchanged_iterations += 1

            if verbose:
                migration_time = time.time() - migration_time_start
                # best_value = calculate_best_value(hall_of_fame)
                print(
                    f"{self.name = } {removed_individuals = } {unchanged_iterations = } {iteration_number = } {migration_time = } {len(hall_of_fame.items)} {len(islands)} {[len(island) for island in islands]}")

            iteration_number += 1

            # Snapshot
            if iteration_number % 100 == 0:
                save_results(self.experiment_name, self.experiment_name + "_snap_", self.iter_number, hall_of_fame,
                             other_collected_data, time.time() - start_time,
                             self.experiment_data)

            # Serialization
            if iteration_number % serialization_frequency == 0:
                filename = "experiment_" + str(self.id)
                serialize_experiment(filename, self.experiment_data, self.key, other_collected_data, islands,
                                     should_run,
                                     hall_of_fame, iteration_number, self.iter_number, self.name, unchanged_iterations)

            other_collected_data.append(
                {"iteration_number": iteration_number, "number_of_islands": len(islands),
                 "time_of_migration:": time.time() - migration_time_start})
            should_run = self.should_still_run(removed_individuals, iteration_number, unchanged_iterations)

        filename = "experiment_" + str(self.id)
        create_done_file(filename)

        return hall_of_fame, other_collected_data
