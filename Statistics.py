from HallOfFame import BasicParetoFront


def print_statistics(population: list, hall_of_fame: BasicParetoFront, iteration_number: int) -> None:
    # for island in population:
    #     for ind in island:
    #         print(ind, f"{ind.fitness=}")
    print("hall of fame in", iteration_number, "iteration:")
    for ind in hall_of_fame:
        print(ind, "fitness", ind.fitness)


def print_statistics_removed(population: list, hall_of_fame: BasicParetoFront, iteration_number: int,
                             removed: int) -> None:
    # for island in population:
    #     for ind in island:
    #         print(ind, f"{ind.fitness=}")
    # print(f"{removed} removed in {iteration_number} iteration:")
    print("removed", removed, "in iteration", iteration_number)


def dont_print_statistics(population: list, hall_of_fame: BasicParetoFront, iteration_number: int, removed: int) -> None:
    pass
