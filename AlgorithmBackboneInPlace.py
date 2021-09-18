import random
import pprint as pp
from typing import Callable

import numpy as np
import matplotlib.pyplot as plt

from deap import base, tools
from HallOfFame import BasicParetoFront


class BasicAlgorithm:

    def __init__(self):
        pass

    def run(self, population: list, logbook: tools.Logbook, stats: tools.Statistics, hall_of_fame: BasicParetoFront,
            update_hall_of_fame: Callable[[base.Toolbox, list, BasicParetoFront],
                                          tuple[BasicParetoFront, int]]) -> [list, tools.Logbook, BasicParetoFront,
                                                                             int]:
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

    def run(self, population: list, logbook: tools.Logbook, stats: tools.Statistics, hall_of_fame: BasicParetoFront,
            update_hall_of_fame: Callable[[base.Toolbox, list, BasicParetoFront],
                                          tuple[BasicParetoFront, int]], dots, fig, island_number) -> [list,
                                                                                                       tools.Logbook,
                                                                                                       int]:

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
                chosen = self.toolbox.clone(chosen)

                if random.random() <= self.crossover_probability:
                    chosen_2 = self.toolbox.select(population, k=1)[0]
                    # TODO can be done better?
                    if hasattr(self, 'optimization_criteria'):
                        chosen[0] = self.toolbox.mate(chosen, chosen_2)
                    else:
                        chosen = self.toolbox.mate(chosen, chosen_2)
                elif random.random() <= self.mutation_probability:
                    chosen = self.toolbox.mutate(chosen)

                del chosen.fitness.values

                fitness = self.toolbox.evaluate(chosen)

                if hasattr(self, 'optimization_criteria'):
                    try:
                        fitness = [fitness[0]['evaluations'][''][crit] for crit in self.optimization_criteria]
                        chosen.fitness.values = fitness
                        offspring.append(chosen)
                    except TypeError:
                        pass
                else:
                    chosen.fitness.values = fitness
                    offspring.append(chosen)

            removed_individuals_partial = update_hall_of_fame(self.toolbox, [offspring, ], hall_of_fame)
            removed_individuals += removed_individuals_partial

            # print(offspring)

            population[:] = offspring

            # record = stats.compile(population)
            # logbook.record(gen=generation, number_of_evaluations=len(invalid_ind), **record)

        # print((population, logbook), hall_of_fame, removed_individuals)

        return population, logbook, removed_individuals


class Nsga2Algorithm(BasicAlgorithm):

    def __init__(self, toolbox: base.Toolbox, mutation_probability: float, crossover_probability: float,
                 number_of_generations: int, *args, **kwargs):
        super().__init__()
        self.toolbox = toolbox
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.number_of_generations = number_of_generations

        if 'optimization_criteria' in kwargs.keys():
            self.optimization_criteria = kwargs['optimization_criteria']

    def run(self, population: list, logbook: tools.Logbook, stats: tools.Statistics, hall_of_fame: BasicParetoFront,
            update_hall_of_fame: Callable[[base.Toolbox, list, BasicParetoFront],
                                          tuple[BasicParetoFront, int]], dots, fig, island_number) -> [list,
                                                                                                       tools.Logbook,
                                                                                                       BasicParetoFront,
                                                                                                       int]:

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitness_results = self.toolbox.map(self.toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitness_results):
            if hasattr(self, 'optimization_criteria'):
                fit = [fit[0]['evaluations'][''][criteria] for criteria in self.optimization_criteria]
            ind.fitness.values = fit

        # record = stats.compile(population)
        # logbook.record(gen=0, number_of_evaluations=len(invalid_ind), **record)

        # Assign pareto fronts
        fronts = tools.sortNondominated(population, len(population))
        for front_number, front in enumerate(fronts):
            for ind in front:
                ind.front_number = front_number

        removed_individuals = 0

        # plt.draw()
        for generation in range(1, self.number_of_generations + 1):

            # Generate offspring:
            # print(f"{generation = }")
            offspring = []

            while len(offspring) < len(population):

                chosen = tools.selTournament(population, k=1, tournsize=2, fit_attr="front_number")[0]
                new_ind = self.toolbox.clone(chosen)

                if random.random() <= self.crossover_probability:
                    chosen_2 = tools.selTournament(population, k=1, tournsize=2, fit_attr="front_number")[0]
                    # TODO can be done better?
                    if hasattr(self, 'optimization_criteria'):
                        new_ind[0] = self.toolbox.mate(chosen, chosen_2)
                        # print("mate", chosen)
                    else:
                        new_ind = self.toolbox.mate(chosen, chosen_2)
                elif random.random() <= self.mutation_probability:
                    if hasattr(self, 'optimization_criteria'):
                        new_ind[0] = self.toolbox.mutate(chosen)
                        # print("mutate", chosen)
                    else:
                        new_ind = self.toolbox.mutate(chosen)

                del new_ind.fitness.values
                # print("del")

                fitness = self.toolbox.evaluate(new_ind)

                if hasattr(self, 'optimization_criteria'):
                    try:
                        fitness = [fitness[0]['evaluations'][''][crit] for crit in self.optimization_criteria]
                        new_ind.fitness.values = fitness
                        offspring.append(new_ind)
                    except TypeError:
                        pass
                        # not appending chosen means it will be calculated again
                        # number_of_unchanged_individuals += 1
                else:
                    new_ind.fitness.values = fitness
                    offspring.append(new_ind)

                # print(offspring)

            # pp.pprint([c.fitness.values for c in offspring])
            # print("--")

            population = self.toolbox.select(population + offspring, len(population))

            # v = []
            # colors = [
            #     "black",
            #     "blue",
            #     "red",
            #     "purple",
            #     "green"
            # ]
            #
            # for hofer in population:
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
            # dots.set_color(colors[island_number])
            # fig.canvas.draw_idle()
            # plt.pause(0.1)

            removed_individuals_partial = update_hall_of_fame(self.toolbox, [population, ], hall_of_fame)
            removed_individuals += removed_individuals_partial

            # record = stats.compile(population)
            # logbook.record(gen=generation, number_of_evaluations=len(invalid_ind), **record)
        # x = input()
        return population, logbook, removed_individuals
