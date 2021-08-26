import random
from typing import Callable

from deap import base, tools


class BasicAlgorithm:

    def __init__(self):
        pass

    def run(self, population: list, logbook: tools.Logbook, stats: tools.Statistics) -> [list, tools.Logbook]:
        pass


class Nsga2Algorithm(BasicAlgorithm):

    def __init__(self, toolbox: base.Toolbox, mutation_probability: float, crossover_probability: float,
                 number_of_generations: int, sort_population: Callable[[list, int], list], *args, **kwargs):
        super().__init__()
        self.toolbox = toolbox
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.number_of_generations = number_of_generations

        self.sort_population = sort_population

        if 'optimization_criteria' in kwargs.keys():
            self.optimization_criteria = kwargs['optimization_criteria']

    def run(self, population: list, logbook: tools.Logbook, stats: tools.Statistics) -> [list, tools.Logbook]:
        # One island run

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitness_results = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        # print(invalid_ind)
        # print(list(fitness_results))
        for ind, fit in zip(invalid_ind, fitness_results):
            if hasattr(self, 'optimization_criteria'):
                fit = [fit[0]['evaluations'][''][criteria] for criteria in self.optimization_criteria]
            ind.fitness.values = fit

        # This is just to assign the crowding distance to the individuals
        # no actual selection is done
        # niepotrzebne jeżeli binary tournament (czyli tournament z k == 2)? wtedy bez DCD wszystko inplace
        population = self.toolbox.select(population, len(population))

        record = stats.compile(population)
        logbook.record(gen=0, number_of_evaluations=len(invalid_ind), **record)

        for generation in range(1, self.number_of_generations + 1):

            number_of_unchanged_individuals = len(population)
            offspring = []

            i = 0
            while number_of_unchanged_individuals > 0:
                # print(f"{i = }")

                # For tournamentDCD it's needed that the population is divisible by 4 when number of individuals
                # to choose is equal to the length of population
                if number_of_unchanged_individuals == len(population):
                    while len(population) % 4 != 0:
                        population.append(population[random.randint(0, len(population) - 1)])

                # Select two parents
                if number_of_unchanged_individuals == 1:
                    number_of_unchanged_individuals = 2

                tmp_offspring = self.sort_population(population, number_of_unchanged_individuals)

                tmp_offspring = [self.toolbox.clone(ind) for ind in tmp_offspring]

                for ind1, ind2 in zip(tmp_offspring[::2], tmp_offspring[1::2]):
                    if random.random() <= self.crossover_probability:
                        # TODO can be done better?
                        if hasattr(self, 'optimization_criteria'):
                            ind1[0], ind2[0] = self.toolbox.mate(ind1, ind2)
                        else:
                            ind1, ind2 = self.toolbox.mate(ind1, ind2)
                    if random.random() <= self.mutation_probability:
                        ind1[0] = self.toolbox.mutate(ind1)
                    if random.random() <= self.mutation_probability:
                        ind2[0] = self.toolbox.mutate(ind2)
                    del ind1.fitness.values, ind2.fitness.values

                # Evaluate the individuals with an invalid fitness
                invalid_ind = [ind for ind in tmp_offspring if not ind.fitness.valid]
                fitness_results = self.toolbox.map(self.toolbox.evaluate, invalid_ind)

                number_of_unchanged_individuals = 0
                for ind, fit in zip(invalid_ind, fitness_results):
                    if hasattr(self, 'optimization_criteria'):
                        try:
                            fit = [fit[0]['evaluations'][''][crit] for crit in self.optimization_criteria]
                            ind.fitness.values = fit
                            offspring.append(ind)
                        except TypeError:
                            number_of_unchanged_individuals += 1

                i += 1

            # Czy to ma sens? Poczytać o NSGA2 bo jak jest tournamentDCD to chyba nie ma sensu nsga2 dodatkowo
            # Czyli bez tournament DCD tylko tam binary tournament i potem robimy selNSGA2 i tam jest używany crowding distance
            population = self.toolbox.select(population + offspring, len(population))

            record = stats.compile(population)
            logbook.record(gen=generation, number_of_evaluations=len(invalid_ind), **record)

        return population, logbook
