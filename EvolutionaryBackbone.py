from typing import Callable

from deap import base
from HallOfFame import BasicParetoFront


class EvolutionaryBackbone:

    def __init__(self,
                 create_population: Callable[[base.Toolbox, ...], list],
                 prepare_population: Callable[[base.Toolbox, list], list],
                 run_algorithm: Callable[[base.Toolbox, list], list],
                 should_still_run: Callable[[list, int, ...], bool],
                 clear_results: Callable[[list], list],
                 prepare_hall_of_fame: Callable[[base.Toolbox, ...], BasicParetoFront],
                 prepare_logs: Callable[[base.Toolbox], list],
                 update_hall_of_fame: Callable[[base.Toolbox, list, BasicParetoFront], BasicParetoFront],
                 update_logs: Callable[[base.Toolbox, list, list], list],
                 toolbox: base.Toolbox,
                 *args, **kwargs):

        self.toolbox = toolbox

        self.create_population = create_population
        self.prepare_population = prepare_population
        self.run_algorithm = run_algorithm

        self.should_still_run = should_still_run
        self.clear_results = clear_results

        self.prepare_hall_of_fame = prepare_hall_of_fame
        self.update_hall_of_fame = update_hall_of_fame

        self.prepare_logs = prepare_logs
        self.update_logs = update_logs

        # args
        self.create_population_args = kwargs['create_population_args']
        self.prepare_hall_of_fame_args = kwargs['prepare_hall_of_fame_args']
        self.should_still_run_args = kwargs['should_still_run_args']

    def run(self) -> tuple[BasicParetoFront, list]:
        should_run = True

        population = self.create_population(self.toolbox, *self.create_population_args)
        population = self.prepare_population(self.toolbox, population)

        hall_of_fame = self.prepare_hall_of_fame(self.toolbox, *self.prepare_hall_of_fame_args)
        logs = self.prepare_logs(self.toolbox)

        iteration_number = 0
        while should_run:
            result = self.run_algorithm(self.toolbox, population)
            should_run = self.should_still_run(result, iteration_number, *self.should_still_run_args)

            population = self.clear_results(result)

            hall_of_fame = self.update_hall_of_fame(self.toolbox, population, hall_of_fame)
            logs = self.update_logs(self.toolbox, population, logs)

            iteration_number += 1

        return hall_of_fame, logs
