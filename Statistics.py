from HallOfFame import BasicParetoFront


def print_statistics(population: list, hall_of_fame: BasicParetoFront) -> None:
    for ind in population[:len(population) // 10]:
        print(ind, f"{ind.fitness=}")
