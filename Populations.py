from deap import base
import pprint as pp


# Population will always be a list of populations

def create_simple_population(toolbox: base.Toolbox, num_of_individuals: int) -> list:
    return [toolbox.population(n=num_of_individuals), ]


def create_islands_population(toolbox: base.Toolbox, num_of_individuals: int, num_of_islands: int) -> list:
    return [toolbox.population(n=num_of_individuals) for _ in range(num_of_islands)]


def population_do_nothing(toolbox: base.Toolbox, population: list) -> list:
    return population
