import random
from typing import Callable

from deap import base


class BasicAlgorithm:

    def __init__(self):
        pass

    def run(self, population: list) -> list:
        pass


class Nsga2Algorithm(BasicAlgorithm):

    def __init__(self, toolbox: base.Toolbox, mutation_probability: float, crossover_probability: float,
                 number_of_generations: int, sort_population: Callable[[list, int], list]):
        super().__init__()
        self.toolbox = toolbox
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.number_of_generations = number_of_generations

        self.sort_population = sort_population

    def run(self, population: list) -> list:

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitness_results = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitness_results):
            ind.fitness.values = fit

        # This is just to assign the crowding distance to the individuals
        # no actual selection is done
        population = self.toolbox.select(population, len(population))

        for generation in range(1, self.number_of_generations + 1):

            offspring = self.sort_population(population, len(population))

            offspring = [self.toolbox.clone(ind) for ind in offspring]

            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                if random.random() <= self.crossover_probability:
                    ind1, ind2 = self.toolbox.mate(ind1, ind2)

                if random.random() <= self.mutation_probability:
                    self.toolbox.mutate(ind1)
                if random.random() <= self.mutation_probability:
                    self.toolbox.mutate(ind2)
                del ind1.fitness.values, ind2.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitness_results = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitness_results):
                ind.fitness.values = fit

            population = self.toolbox.select(population + offspring, len(population))

        return population
