from typing import Callable
import pprint as pp
import numpy as np
import time

from deap import base, tools
from HallOfFame import BasicParetoFront
from utils import save_results, serialize_experiment, create_done_file, calculate_best_value


class EvolutionaryBackbone:

    def __init__(self,
                 create_population,
                 run_algorithm,
                 migrate,
                 should_still_run,
                 clear_results,
                 prepare_hall_of_fame,
                 prepare_logs,
                 update_hall_of_fame,
                 print_statistics,
                 toolbox,
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
        old_time = exp.old_time

        return experiment_data, key, other_data, populations, should_run, hall_of_fame, iteration_number, iter_number, name, iters, old_time

    def prepare_run(self):
        should_run = True
        populations = self.create_population(self.toolbox)
        hall_of_fame = self.prepare_hall_of_fame(self.toolbox)
        iteration_number = 0
        other_data = []
        unchanged_iterations = 0
        old_time = 0.0

        return should_run, populations, hall_of_fame, iteration_number, other_data, unchanged_iterations, old_time

    def run(self, verbose=False, exp=None):
        if exp:
            self.experiment_data, self.key, other_collected_data, islands, should_run, hall_of_fame, iteration_number, self.iter_number, self.name, unchanged_iterations, old_time = self.resolve_exp(
                exp)
        else:
            should_run, islands, hall_of_fame, iteration_number, other_collected_data, unchanged_iterations, old_time = self.prepare_run()

        serialization_frequency = 5
        direction = self.toolbox.direction.keywords['direction']
        start_time = time.time()

        while should_run:
            # print("Runned")
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
                print("self.name =", self.name, "removed_individuals =", removed_individuals, "unchanged_iterations =", unchanged_iterations)
                print("iteration_number =", iteration_number, "migration_time =", migration_time)
                len_hall_of_fame = len(hall_of_fame.items)
                number_of_islands = len(islands)
                islands_sizes = [len(island) for island in islands]
                print("len_hall_of_fame =", len_hall_of_fame, "number_of_islands =", number_of_islands, "islands_sizes =", islands_sizes)
                print("time", old_time + (time.time() - start_time))

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
                                     hall_of_fame, iteration_number, self.iter_number, self.name, unchanged_iterations, old_time + (time.time() - start_time))

            other_collected_data.append(
                {"iteration_number": iteration_number, "number_of_islands": len(islands),
                 "time_of_migration:": time.time() - migration_time_start})
            should_run = self.should_still_run(removed_individuals, iteration_number, unchanged_iterations)

        filename = "experiment_" + str(self.id)
        create_done_file(filename)

        return hall_of_fame, other_collected_data, old_time + (time.time() - start_time)
