import random
import pprint as pp
from typing import Callable

from deap import base, tools


class BasicAlgorithm:

    def __init__(self):
        pass

    def run(self, population: list) -> list:
        pass


class Nsga2Algorithm(BasicAlgorithm):

    def __init__(self, toolbox: base.Toolbox, mutation_probability: float, crossover_probability: float,
                 number_of_generations: int, select_from_population: Callable[[list, int], list],
                 check_correction: Callable[[list], list], *args, **kwargs):
        super().__init__()
        self.toolbox = toolbox
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.number_of_generations = number_of_generations
        self.check_correction = check_correction

        self.select_from_population = select_from_population

        if 'optimization_criteria' in kwargs.keys():
            self.optimization_criteria = kwargs['optimization_criteria']

    def run(self, population: list) -> list:

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
        # population = self.toolbox.select(population, len(population))
        tools.assignCrowdingDist(population)

        for generation in range(1, self.number_of_generations + 1):

            # For tournamentDCD it's needed that the population is divisible by 4
            # while len(population) % 4 != 0:
            #     population.append(population[random.randint(0, len(population) - 1)])

            offspring = self.select_from_population(population, 2)

            offspring = [self.toolbox.clone(ind) for ind in offspring]

            # TODO for frams it should be ind1[0] = blah_blah
            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                if random.random() <= self.crossover_probability:
                    ind1[0] = self.toolbox.mate(ind1, ind2)

                if random.random() <= self.mutation_probability:
                    ind1[0] = self.toolbox.mutate(ind1)
                del ind1.fitness.values, ind2.fitness.values

            # Evaluate the individuals with an invalid fitness
            # TODO Sometimes evaluation is NONE. Repeat in wrapper until it's fine?
            # TODO Repeating does not work. Should check why
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitness_results = self.toolbox.map(self.toolbox.evaluate, invalid_ind)

            for ind, fit in zip(invalid_ind, fitness_results):
                if hasattr(self, 'optimization_criteria'):
                    try:
                        fit = [fit[0]['evaluations'][''][criteria] for criteria in self.optimization_criteria]
                    except:
                        print(invalid_ind)
                        print(fit)
                ind.fitness.values = fit

            population = self.toolbox.select(population + offspring, len(population))

        return population
