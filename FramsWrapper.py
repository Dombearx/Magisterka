from framsticks.new_frams.FramsticksLib import FramsticksLib


def wrapper_get_simplest(cli: FramsticksLib, genetic_format: int) -> str:
    genotype = cli.getSimplest(genetic_format)

    return genotype


def wrapper_mutate(cli: FramsticksLib, genotype_list: list[str]) -> str:
    genotype = cli.mutate(genotype_list)

    return genotype[0]


def wrapper_evaluate(cli: FramsticksLib, genotype_list: list[str]) -> dict:
    results = cli.evaluate(genotype_list)

    while results[0]['evaluations'] is None:
        print("Found None")
        print(genotype_list)
        # Not working: C(LLRX[|, p:0.25, r:1][|]X[|, p:0.1], )

        results = cli.evaluate(genotype_list)

    return results


def wrapper_crossover(cli: FramsticksLib, genotype_parent1: list, genotype_parent2: list) -> tuple[str, str]:
    genotype1 = cli.crossOver(genotype_parent1[0], genotype_parent2[0])
    genotype2 = cli.crossOver(genotype_parent2[0], genotype_parent1[0])

    return genotype1, genotype2
