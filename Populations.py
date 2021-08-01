from deap import base
import pprint as pp

# Population will always be a list of populations

def create_simple_population(toolbox: base.Toolbox, n_individuals: int) -> list:
    return [toolbox.population(n=n_individuals), ]


def create_islands_population(toolbox: base.Toolbox, n_individuals: int, islands_number: int) -> list:
    return [toolbox.population(n=n_individuals) for _ in range(islands_number)]


def population_do_nothing(toolbox: base.Toolbox, population: list) -> list:
    return population


def clear_do_nothing(population: list) -> list:
    return population


def clear_population(populations: list) -> list:
    # print(zip(*population))
    # zipped = list(map(list, zip(*population)))
    # islands = zipped[0]
    # print("islands", islands)

    return list(populations)
