from __future__ import division
import random
from deap import tools, creator, benchmarks
import statistics


def assignCrowdingDist(individuals):
    """Assign a crowding distance to each individual's fitness. The
    crowding distance can be retrieve via the :attr:`crowding_dist`
    attribute of each individual's fitness.
    """
    if len(individuals) == 0:
        return

    distances = [0.0] * len(individuals)
    crowd = [(ind.fitness.values, i) for i, ind in enumerate(individuals)]

    nobj = len(individuals[0].fitness.values)

    for i in range(nobj):
        crowd.sort(key=lambda element: element[0][i])
        distances[crowd[0][1]] = float("inf")
        distances[crowd[-1][1]] = float("inf")
        if crowd[-1][0][i] == crowd[0][0][i]:
            continue
        norm = nobj * float(crowd[-1][0][i] - crowd[0][0][i])
        for prev, cur, next in zip(crowd[:-2], crowd[1:-1], crowd[2:]):
            distances[cur[1]] += (next[0][i] - prev[0][i]) / norm

    for i, dist in enumerate(distances):
        individuals[i].fitness.crowding_dist = dist


# sortuje według fitness niemalejąco
# do selekcji konwekcyjnej dla problemów jednokryterialnych
def sort_by_fitness(population: list, direction) -> list:
    if direction == "min":
        reverse = False
    else:
        reverse = True
    population = sorted(population, key=lambda x: x.fitness, reverse=reverse)

    return population


# Migracja frontami pareto ze stałą liczbą wysp

def migrate_const_islands(population: list, direction, number_of_islands: int) -> list:
    whole_population = [ind for island in population for ind in island]
    assignCrowdingDist(whole_population)

    pareto_fronts = tools.sortNondominated(whole_population, len(whole_population))

    fronts = []

    for front in pareto_fronts:
        fronts.append(sorted(front, key=lambda x: x.fitness.crowding_dist, reverse=True))

    pareto_fronts = fronts

    # SORT BY FITNESS MIN OR MAX

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


def migrate_const_islands_overleap(population: list, direction, number_of_islands: int) -> list:
    whole_population = [ind for island in population for ind in island]
    assignCrowdingDist(whole_population)

    max_size = 150

    pareto_fronts = tools.sortNondominated(whole_population, len(whole_population))

    fronts = []

    for front in pareto_fronts:
        fronts.append(sorted(front, key=lambda x: x.fitness.crowding_dist, reverse=True))

    pareto_fronts = fronts

    if len(pareto_fronts) > 1:
        better_fronts_size = sum([len(front) for front in pareto_fronts[:-1]])
    else:
        better_fronts_size = 0

    pareto_fronts[-1] = pareto_fronts[-1][:max_size - better_fronts_size]

    assert(sum([len(front) for front in pareto_fronts]) == max_size)

    #OVERLEAP

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


def migrate_const_islands_different_sizes(population: list, direction, number_of_islands: int) -> list:
    whole_population = [ind for island in population for ind in island]
    assignCrowdingDist(whole_population)

    pareto_fronts = tools.sortNondominated(whole_population, len(whole_population))

    fronts = []

    for front in pareto_fronts:
        fronts.append(sorted(front, key=lambda x: x.fitness.crowding_dist, reverse=True))

    pareto_fronts = fronts

    whole_population = [ind for island in pareto_fronts for ind in island]
    basic_island_size = int(len(whole_population) / number_of_islands)

    new_islands = []
    sizes = [50, 40, 30, 20, 10]
    assert (sum(sizes) == len(whole_population))
    index = 0
    for size in sizes:
        new_islands.append(whole_population[index:index + size])
        index += size

    # last_index = len(whole_population) - (len(whole_population) % island_size)
    #
    # # Add extra individuals to the last island
    # if last_index < len(whole_population):
    #     new_islands[-1] += whole_population[last_index + 1:]

    return new_islands


# Migracja między wyspami w selekcji konwekcyjnej dla problemów WIELOKRYTERIALNYCH

# TODO Check if it is correct
def migrate_one_front_one_island(population: list, direction) -> list:
    whole_population = [ind for island in population for ind in island]
    pareto_fronts = tools.sortNondominated(whole_population, len(whole_population))

    return pareto_fronts


# Migracja między wyspami w selekcji konwekcyjnej dla problemów JEDNOKRYTERIALNYCH

def migrate_const_islands_one_criteria(population: list, direction, number_of_islands: int) -> list:
    whole_population = [ind for island in population for ind in island]
    island_size = int(len(whole_population) / number_of_islands)

    new_islands = []
    whole_population = sort_by_fitness(whole_population, direction)

    for i in range(0, len(whole_population), island_size):
        new_islands.append(whole_population[i:i + island_size])

    last_index = len(whole_population) - (len(whole_population) % island_size)

    # Add extra individuals to the last island
    if last_index < len(whole_population):
        new_islands[-1] += whole_population[last_index + 1:]

    return new_islands


def migrate_random(population: list, direction, number_of_islands: int) -> list:
    whole_population = [ind for island in population for ind in island]
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

    return new_islands
