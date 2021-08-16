from HallOfFame import BasicParetoFront


def print_statistics(population: list, hall_of_fame: BasicParetoFront, iteration_number: int, logs: list) -> None:
    # for island in population:
    #     for ind in island:
    #         print(ind, f"{ind.fitness=}")
    print("hall of fame:")
    for ind in hall_of_fame:
        print(ind, f"{ind.fitness=}")
