from HallOfFame import BasicParetoFront


def print_statistics(population: list, hall_of_fame: BasicParetoFront) -> None:
    for island in population:
        for ind in island[:len(island) // 10]:
            print(ind, f"{ind.fitness=}")
