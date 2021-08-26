import random
import pprint as pp
from typing import Callable

from deap import base, tools


class BasicAlgorithm:

    def __init__(self):
        pass

    def run(self, population: list, logbook: tools.Logbook, stats: tools.Statistics) -> [list, tools.Logbook]:
        pass


class Nsga2Algorithm(BasicAlgorithm):

    def __init__(self, toolbox: base.Toolbox, mutation_probability: float, crossover_probability: float,
                 number_of_generations: int, select_from_population: Callable[[list, int], list], *args, **kwargs):
        super().__init__()
        self.toolbox = toolbox
        self.mutation_probability = mutation_probability
        self.crossover_probability = crossover_probability
        self.number_of_generations = number_of_generations

        self.select_from_population = select_from_population

        if 'optimization_criteria' in kwargs.keys():
            self.optimization_criteria = kwargs['optimization_criteria']

    def run(self, population: list, logbook: tools.Logbook, stats: tools.Statistics) -> [list, tools.Logbook]:

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitness_results = self.toolbox.map(self.toolbox.evaluate, invalid_ind)

        for ind, fit in zip(invalid_ind, fitness_results):
            if hasattr(self, 'optimization_criteria'):
                fit = [fit[0]['evaluations'][''][criteria] for criteria in self.optimization_criteria]
            ind.fitness.values = fit

        record = stats.compile(population)
        logbook.record(gen=0, number_of_evaluations=len(invalid_ind), **record)

        # Assign pareto fronts
        fronts = tools.sortNondominated(population, len(population))
        for front_number, front in enumerate(fronts):
            for ind in front:
                ind.front_number = front_number

        for generation in range(1, self.number_of_generations + 1):
            # Generate offspring:
            print(f"{generation = }")
            offspring = []

            while len(offspring) < len(population):

                chosen = tools.selTournament(population, k=1, tournsize=2, fit_attr="front_number")[0]
                chosen = self.toolbox.clone(chosen)

                if random.random() <= self.crossover_probability:
                    chosen_2 = tools.selTournament(population, k=1, tournsize=2, fit_attr="front_number")[0]
                    # TODO can be done better?
                    if hasattr(self, 'optimization_criteria'):
                        chosen[0] = self.toolbox.mate(chosen, chosen_2)
                    else:
                        chosen = self.toolbox.mate(chosen, chosen_2)
                elif random.random() <= self.mutation_probability:
                    chosen[0] = self.toolbox.mutate(chosen)

                del chosen.fitness.values

                fitness = self.toolbox.evaluate(chosen)

                if hasattr(self, 'optimization_criteria'):
                    try:
                        fitness = [fitness[0]['evaluations'][''][crit] for crit in self.optimization_criteria]
                        chosen.fitness.values = fitness
                        offspring.append(chosen)
                    except TypeError:
                        pass
                        # number_of_unchanged_individuals += 1
                else:
                    chosen.fitness.values = fitness
                    offspring.append(chosen)

                print(offspring)

            population = self.toolbox.select(population + offspring, len(population))

            record = stats.compile(population)
            logbook.record(gen=generation, number_of_evaluations=len(invalid_ind), **record)

        return population, logbook
