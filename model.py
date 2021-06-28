import numpy as np

from deap import tools
from wielokryterialne.nsga2_alg import nsga2Algorithm, myParetoFront
from wielokryterialne.benchmarks_conf import getDTLZ1ToolBox, getDTLZ2ToolBox, getDTLZ3ToolBox, getDTLZ4ToolBox
from wielokryterialne.migration import migSelFrontsContsInslands, migSelOneFrontOneIsland, migIslandsRandom

BENCHMARKS = {
    "dtlz1": getDTLZ1ToolBox,
    "dtlz2": getDTLZ2ToolBox,
    "dtlz3": getDTLZ3ToolBox,
    "dtlz4": getDTLZ4ToolBox
}

MIGRATION_METHODS = {
    "convection_const": migSelFrontsContsInslands,
    "convection_front": migSelOneFrontOneIsland,
    "island": migIslandsRandom
}


def get_benchmarks_names() -> list[str]:
    return list(BENCHMARKS.keys())


def get_migration_methods() -> list[str]:
    return list(MIGRATION_METHODS.keys())


class Model:

    def __init__(self, benchmark_name: str, num_of_islands: int, migration_ratio: float, migration_method: str,
                 num_of_benchmark_objectives: int, population_size: int, max_iterations_wo_improvement: int,
                 register_statistics: bool):

        self.FREQ = int(migration_ratio * population_size)
        self.CXPB, self.MUTPB = 0.1, 1.0
        self.max_iterations_wo_improvement = max_iterations_wo_improvement

        self.toolbox = BENCHMARKS[benchmark_name](num_of_benchmark_objectives)

        self.toolbox.register("map", map)

        if register_statistics:
            self.__register_statistics()

        self.__create_hall_of_fame()

        self.__select_migtaion_method(migration_method, num_of_islands)

        self.init_population(int(population_size/ num_of_islands), num_of_islands)



    def __register_statistics(self):
        # Statistics
        self.stats = tools.Statistics(lambda ind: ind.fitness.values)
        self.stats.register("avg", np.mean, axis=0)
        self.stats.register("std", np.std, axis=0)
        self.stats.register("min", np.min, axis=0)
        self.stats.register("max", np.max, axis=0)

    def __create_hall_of_fame(self):

        self.hallOfFame = myParetoFront(100)

    def __select_migtaion_method(self, method, num_of_islands):
        self.toolbox.register("migrate", MIGRATION_METHODS[method],
                              numOfIslands=num_of_islands)

    def init_population(self, island_population_size, num_of_islands):

        # Początkowa populacja
        self.islands = [self.toolbox.population(n=island_population_size)
                        for i in range(num_of_islands)]

        # ngen = FREQ oznacza ile wykonań algorytmu się wykona przy jednym uruchomieniu funkcji
        self.toolbox.register("algorithm", nsga2Algorithm, toolbox=self.toolbox,
                              stats=self.stats, cxpb=self.CXPB, mutpb=self.MUTPB, ngen=self.FREQ, verbose=False,
                              halloffame=self.hallOfFame)

    def run(self):
        iterations_wo_improvement = 0
        self.best_individuals = []
        self.logbooks = []

        self.toolbox.migrate(self.islands)
        first = True

        while (iterations_wo_improvement <= self.max_iterations_wo_improvement / self.FREQ):

            results = self.toolbox.map(self.toolbox.algorithm, self.islands)

            ziped = list(map(list, zip(*results)))
            self.islands = ziped[0]

            removed = ziped[2]

            sum_removed = sum(removed)

            if sum_removed <= 0:
                iterations_wo_improvement += 1
            else:
                iterations_wo_improvement = 0
                print("Removed: ", sum_removed,
                      "Improvement: ", self.hallOfFame[0].fitness)

            # if (iterations_wo_improvement * FREQ % int(max_iterations_wo_improvement / 10) == 0):
            #     print("iterations_wo_improvement:", (iterations_wo_improvement *
            #                                          FREQ / max_iterations_wo_improvement) * 100, "%  time:",
            #           round(time.time() - mig_start_time, 2))
            #     mig_start_time = time.time()

            bestInMigration = []
            for ind in self.hallOfFame:
                bestInMigration.append(ind.fitness.values)

            self.best_individuals.append(bestInMigration)

            if first:
                for logbook in ziped[1]:
                    self.logbooks.append(logbook)
                first = False
            else:
                for k, logbook in enumerate(ziped[1]):
                    self.logbooks[k] += logbook

            self.toolbox.migrate(self.islands)

# first = True
# previous_pareto_front = None
#
# print("Running:", BENCHMARK_NAME)
# print("Islands number:", NUM_OF_ISLANDS)
# print("Migration every", FREQ, "steps")
# print("Max iterations without improvement:", max_iterations_wo_improvement)
# print("Model:", MODEL)
# print("----------START---------")
# mig_start_time = time.time()
#
#
# print("----------END---------")
# print("Hall of fame[0]:", hallOfFame[0], hallOfFame[0].fitness)
#
# # Save results
# pickleOut = open("./out/" + BENCHMARK_NAME + "_" + str(NUM_OF_ISLANDS) +
#                  "_" + str(MIGRATION_RATIO) + "_" + MODEL + "_" + str(NUM_OF_OBJECTIVES) + ".pickle", "wb")
# pickle.dump(utils.result(
#     logbooks, bestIndividuals, time.time() - start_time), pickleOut)
# pickleOut.close()
#
# print("\n")
