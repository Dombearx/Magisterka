from __future__ import division
import random
from deap import tools, creator
import statistics


# sortuje według fitness niemalejąco
# do selekcji konwekcyjnej dla problemów jednokryterialnych

def sort_by_fitness(population: list) -> list:
    population = sorted(population, key=lambda x: x.fitness, reverse=False)

    return population


# TODO when new_islands.append happen the reference is used, therefore population[i] = new_island doesn't work correctly
# Migracja frontami pareto ze stałą liczbą wysp

def migrate_const_islands(population: list, number_of_islands: int) -> list:
    whole_population = [ind for island in population for ind in island]
    pareto_fronts = tools.sortNondominated(whole_population, len(whole_population))

    whole_population = [ind for island in pareto_fronts for ind in island]
    island_size = int(len(whole_population) / number_of_islands)

    new_islands = []
    for i in range(0, len(whole_population), island_size):
        new_islands.append(whole_population[i:i + island_size])

    last_index = len(whole_population) - (len(whole_population) % island_size)

    # Add extra individuals to the last island
    if last_index < len(whole_population):
        new_islands[-1] += whole_population[last_index + 1:]

    return new_islands


# Migracja między wyspami w selekcji konwekcyjnej dla problemów WIELOKRYTERIALNYCH

def migrate_one_front_one_island(population: list) -> list:
    whole_population = []

    for island in population:
        whole_population += island

    pareto_fronts = tools.sortNondominated(whole_population, len(whole_population))

    for i, new_island in enumerate(pareto_fronts):
        if i >= len(population):
            population.append(new_island)
        else:
            population[i] = new_island

    if len(population) > len(pareto_fronts):
        del population[len(pareto_fronts):]

    return population


# Migracja między wyspami w selekcji konwekcyjnej dla problemów JEDNOKRYTERIALNYCH

def migrate_const_islands_one_criteria(population: list, number_of_islands: int) -> list:
    whole_population = []

    for island in population:
        whole_population += island

    island_size = int(len(whole_population) / number_of_islands)

    new_islands = []

    whole_population = sort_by_fitness(whole_population)

    for i in range(0, len(whole_population), island_size):
        new_islands.append(whole_population[i:i + island_size])

    last_index = len(whole_population) - (len(whole_population) % island_size)

    # Add extra individuals to the last island
    if last_index < len(whole_population):
        new_islands[-1] += whole_population[last_index + 1:]

    new_islands[-1] += whole_population[last_index:]

    for i, new_island in enumerate(new_islands):
        if i >= len(population):
            population.append(new_island)
        else:
            population[i] = new_island

    if len(population) > len(new_islands):
        del population[len(new_islands):]

    return population


def migrate_random(population: list, number_of_islands: int) -> list:
    whole_population = []

    for island in population:
        whole_population += island

    island_size = int(len(whole_population) / number_of_islands)

    new_islands = []

    # Shuffle population
    whole_population = random.sample(whole_population, len(whole_population))

    for i in range(0, len(whole_population), island_size):
        new_islands.append(whole_population[i:i + island_size])

    last_index = len(whole_population) - (len(whole_population) % island_size)

    # Add extra individuals to the last island
    if last_index < len(whole_population):
        new_islands[-1] += whole_population[last_index + 1:]

    new_islands[-1] += whole_population[last_index:]

    new_islands[-1] += whole_population[last_index:]

    for i, new_island in enumerate(new_islands):
        if i >= len(population):
            population.append(new_island)
        else:
            population[i] = new_island

    if len(population) > len(new_islands):
        del population[len(new_islands):]

    return population
