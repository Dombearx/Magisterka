from typing import Callable

from deap import base


class EvolutionaryBackbone:

    def __init__(self,
                 create_population: Callable[[base.Toolbox, ...], list],
                 prepare_population: Callable[[base.Toolbox, list], list],
                 run_algorithm: Callable[[base.Toolbox, list], list],
                 should_still_run: Callable[[list], bool],
                 clear_results: Callable[[list], list],
                 prepare_hall_of_fame: Callable[[base.Toolbox], list],
                 prepare_logs: Callable[[base.Toolbox], list],
                 update_hall_of_fame: Callable[[base.Toolbox, list, list], list],
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

        #args
        self.create_population_args = kwargs['create_population']

    def run(self) -> tuple[list, list]:
        should_run = True

        population = self.create_population(self.toolbox, *self.create_population_args)
        population = self.prepare_population(self.toolbox, population)

        hall_of_fame = self.prepare_hall_of_fame(self.toolbox)
        logs = self.prepare_logs(self.toolbox)

        while should_run:
            result = self.run_algorithm(self.toolbox, population)
            should_run = self.should_still_run(result)

            population = self.clear_results(result)

            hall_of_fame = self.update_hall_of_fame(self.toolbox, population, hall_of_fame)
            logs = self.update_logs(self.toolbox, population, logs)

        return hall_of_fame, logs
