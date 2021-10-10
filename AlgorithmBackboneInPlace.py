import random
import pprint as pp
from typing import Callable

import numpy as np
import time

from deap import base, tools
from HallOfFame import BasicParetoFront


class BasicAlgorithm:

    def __init__(self):
        pass

    def run(self, population: list, hall_of_fame: BasicParetoFront,
            update_hall_of_fame):
        pass


class SimpleOneCriteriaAlgorithm(BasicAlgorithm):
    def __init__(self, toolbox: base.Toolbox, mutation_probability: float, crossover_probability: float,
                 number_of_generations: int, *args, **kwargs):
        super().__init__()
        self.toolbox = toolbox
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.number_of_generations = number_of_generations

        if 'optimization_criteria' in kwargs.keys():
            self.optimization_criteria = kwargs['optimization_criteria']

    def run(self, population: list, hall_of_fame: BasicParetoFront,
            update_hall_of_fame):

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitness_results = self.toolbox.map(self.toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitness_results):
            if hasattr(self, 'optimization_criteria'):
                fit = [fit[0]['evaluations'][''][criteria] for criteria in self.optimization_criteria]
            ind.fitness.values = fit

        # record = stats.compile(population)
        # logbook.record(gen=0, number_of_evaluations=len(invalid_ind), **record)

        removed_individuals = 0
        for generation in range(1, self.number_of_generations + 1):
            offspring = []
            # print(f"{generation=}")
            while len(offspring) < len(population):

                chosen = self.toolbox.select(population, k=1)[0]
                new_ind = self.toolbox.clone(chosen)

                if random.random() <= self.crossover_probability:
                    chosen_2 = self.toolbox.select(population, k=1)[0]
                    new_ind_2 = self.toolbox.clone(chosen_2)
                    # TODO can be done better?
                    if hasattr(self, 'optimization_criteria'):
                        new_ind[0] = self.toolbox.mate(new_ind, new_ind_2)
                    else:
                        new_ind = self.toolbox.mate(new_ind, new_ind_2)
                elif random.random() <= self.mutation_probability:
                    if hasattr(self, 'optimization_criteria'):
                        new_ind[0] = self.toolbox.mutate(new_ind)
                    else:
                        new_ind = self.toolbox.mutate(new_ind)

                del new_ind.fitness.values

                fitness = self.toolbox.evaluate(new_ind)

                if hasattr(self, 'optimization_criteria'):
                    try:
                        fitness = [fitness[0]['evaluations'][''][crit] for crit in self.optimization_criteria]
                        new_ind.fitness.values = fitness
                        offspring.append(new_ind)
                    except TypeError:
                        pass
                else:
                    new_ind.fitness.values = fitness
                    offspring.append(new_ind)

            removed_individuals_partial = update_hall_of_fame(self.toolbox, [offspring, ], hall_of_fame)
            removed_individuals += removed_individuals_partial

            # print(offspring)

            population[:] = offspring

            # record = stats.compile(population)
            # logbook.record(gen=generation, number_of_evaluations=len(invalid_ind), **record)

        # print((population, logbook), hall_of_fame, removed_individuals)

        return population, removed_individuals

class Nsga2Algorithm(BasicAlgorithm):

    def check_validaty(self, fitness):
        params = fitness[0]['evaluations']['']
        if params["numparts"] > 20:
            return False
        if params["numneurons"] > 20:
            return False
        if params["numjoints"] > 30:
            return False
        if params["numconnections"] > 30:
            return False
        return True

    def __init__(self, toolbox: base.Toolbox, mutation_probability: float, crossover_probability: float,
                 number_of_generations: int, *args, **kwargs):
        super().__init__()
        self.toolbox = toolbox
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.number_of_generations = number_of_generations

        if 'optimization_criteria' in kwargs.keys():
            self.optimization_criteria = kwargs['optimization_criteria']

    def run(self, population: list, hall_of_fame: BasicParetoFront,
            update_hall_of_fame):

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitness_results = self.toolbox.map(self.toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitness_results):
            if hasattr(self, 'optimization_criteria'):
                fit = [fit[0]['evaluations'][''][criteria] for criteria in self.optimization_criteria]
            ind.fitness.values = fit

        # record = stats.compile(population)
        # logbook.record(gen=0, number_of_evaluations=len(invalid_ind), **record)

        removed_individuals = 0

        for generation in range(1, self.number_of_generations + 1):
            t = time.time()

            # Assign pareto fronts
            fronts = tools.sortNondominated(population, len(population))
            for front_number, front in enumerate(reversed(fronts)):
                for ind in front:
                    ind.front_number = front_number
            if len(fronts) > 1:
                pass

            offspring = []

            while len(offspring) < len(population):

                chosen = tools.selTournament(population, k=1, tournsize=2, fit_attr="front_number")[0]
                new_ind = self.toolbox.clone(chosen)

                if random.random() <= self.crossover_probability:
                    chosen_2 = tools.selTournament(population, k=1, tournsize=2, fit_attr="front_number")[0]
                    new_ind_2 = self.toolbox.clone(chosen_2)
                    # TODO can be done better?
                    if hasattr(self, 'optimization_criteria'):
                        new_ind[0] = self.toolbox.mate(new_ind, new_ind_2)
                    else:
                        new_ind = self.toolbox.mate(new_ind, new_ind_2)
                elif random.random() <= self.mutation_probability:
                    if hasattr(self, 'optimization_criteria'):
                        new_ind[0] = self.toolbox.mutate(new_ind)
                    else:
                        new_ind = self.toolbox.mutate(new_ind)

                del new_ind.fitness.values

                fitness = self.toolbox.evaluate(new_ind)

                if hasattr(self, 'optimization_criteria'):
                    try:
                        if self.check_validaty(fitness):
                            fitness = [fitness[0]['evaluations'][''][crit] for crit in self.optimization_criteria]
                            new_ind.fitness.values = fitness
                            offspring.append(new_ind)
                    except TypeError:
                        # print("error occured")
                        pass
                        # not appending chosen means it will be calculated again
                else:
                    new_ind.fitness.values = fitness
                    offspring.append(new_ind)

            population = self.toolbox.select(population + offspring, len(population))

            removed_individuals_partial = update_hall_of_fame(self.toolbox, [population, ], hall_of_fame)
            removed_individuals += removed_individuals_partial
            geneartion_time = time.time() - t
            # print("generation:", generation, "geneartion_time:", geneartion_time)
            # print(f"{generation = } {time.time() - t} {removed_individuals_partial = }")

            # record = stats.compile(population)
            # logbook.record(gen=generation, number_of_evaluations=len(invalid_ind), **record)

        return population, removed_individuals
