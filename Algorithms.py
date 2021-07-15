import random

from deap import base, tools


class NSGA2:
    def __init__(self, number_of_generations, crossover_probability, mutation_probability):
        self.number_of_generations = number_of_generations
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability

    def run(self, toolbox: base.Toolbox, population: list) -> list:
        # logbook = tools.Logbook()
        # logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # if halloffame is not None:
        #     halloffame.update(population)

        number_of_individuals = len(population)

        # This is just to assign the crowding distance to the individuals
        # no actual selection is done
        population = toolbox.select(population, len(population))

        # record = stats.compile(population) if stats else {}
        # logbook.record(gen=0, evals=len(invalid_ind), **record)
        #
        # if verbose:
        #     print(logbook.stream)
        # Begin the generational process

        for gen in range(1, self.number_of_generations + 1):
            # Vary the population

            # Dodawanie osobników aż populacja będzie podzielna przez 4
            while len(population) % 4 != 0:
                population.append(
                    population[random.randint(0, len(population) - 1)])

            offspring = tools.selTournamentDCD(population, len(population))

            offspring = [toolbox.clone(ind) for ind in offspring]

            for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
                if random.random() <= self.crossover_probability:
                    ind1, ind2 = toolbox.mate(ind1, ind2)

                if random.random() <= self.mutation_probability:
                    toolbox.mutate(ind1)
                if random.random() <= self.mutation_probability:
                    toolbox.mutate(ind2)
                del ind1.fitness.values, ind2.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # if halloffame is not None:
            #     removed += halloffame.update(offspring)

            # Select the next generation population
            population = toolbox.select(population + offspring, number_of_individuals)
            # record = stats.compile(population) if stats else {}
            # logbook.record(gen=gen, evals=len(invalid_ind), **record)
            # if verbose:
            #     print(logbook.stream)
        return [population, offspring]
