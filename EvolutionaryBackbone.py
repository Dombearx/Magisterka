from typing import Callable
import pprint as pp

from deap import base, tools
from HallOfFame import BasicParetoFront


class EvolutionaryBackbone:

    def __init__(self,
                 create_population: Callable[[base.Toolbox, ...], list],
                 run_algorithm: Callable[[list, tools.Logbook, tools.Statistics], tuple[list, list]],
                 migrate: Callable[[list, ...], list],
                 should_still_run: Callable[[int, int, ...], bool],
                 clear_results: Callable[[list], list],
                 prepare_hall_of_fame: Callable[[base.Toolbox, ...], BasicParetoFront],
                 prepare_logs: Callable[[base.Toolbox, ...], tuple[list, tools.Statistics]],
                 update_hall_of_fame: Callable[[base.Toolbox, list, BasicParetoFront], tuple[BasicParetoFront, int]],
                 update_logs: Callable[[base.Toolbox, list, list], list],
                 print_statistics: Callable[[list, BasicParetoFront, int, ...], None],
                 toolbox: base.Toolbox,
                 *args, **kwargs):
        self.toolbox = toolbox

        self.create_population = create_population
        self.run_algorithm = run_algorithm

        self.should_still_run = should_still_run
        self.clear_results = clear_results

        self.prepare_hall_of_fame = prepare_hall_of_fame
        self.update_hall_of_fame = update_hall_of_fame

        self.prepare_logs = prepare_logs
        self.update_logs = update_logs

        self.print_statistics = print_statistics

        self.migrate = migrate

    def run(self) -> tuple[BasicParetoFront, list]:
        should_run = True

        populations = self.create_population(self.toolbox)

        hall_of_fame = self.prepare_hall_of_fame(self.toolbox)
        logs, stats = self.prepare_logs(self.toolbox)

        iteration_number = 0

        while should_run:

            populations = self.migrate(populations)

            result = self.toolbox.map(lambda population, log: self.run_algorithm(population, log, stats), populations, logs)

            populations, logs = self.clear_results(result)

            hall_of_fame, removed_individuals = self.update_hall_of_fame(self.toolbox, populations, hall_of_fame)

            # TODO Remove? Does nothing for now
            logs = self.update_logs(self.toolbox, populations, logs)

            self.print_statistics(populations, hall_of_fame, iteration_number, logs)
            iteration_number += 1

            should_run = self.should_still_run(removed_individuals, iteration_number)

        return hall_of_fame, logs
