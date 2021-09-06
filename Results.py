import pprint as pp


def clear_do_nothing(population: list) -> list:
    return population


def clear_population(results: list) -> [list, list]:
    populations, logs, removed_individuals = zip(*results)
    # print(zip(*population))
    # zipped = list(map(list, zip(*population)))
    # islands = zipped[0]
    # print("islands", islands)

    return list(populations), list(logs), sum(removed_individuals)
