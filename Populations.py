from deap import base


def create_simple_population(toolbox: base.Toolbox, n_individuals: int) -> list:
    return toolbox.population(n=n_individuals)


def create_islands_population(toolbox: base.Toolbox, n_individuals: int, islands_number: int) -> list:
    return [toolbox.population(n=n_individuals) for _ in range(islands_number)]


def do_nothing(toolbox: base.Toolbox, population: list) -> list:
    return population
