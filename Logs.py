from deap import base, tools
import numpy as np


def prepare_standard_logbook(toolbox: base.Toolbox, number_of_islands: int) -> [list, tools.Statistics]:
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean, axis=0)
    stats.register("std", np.std, axis=0)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    logbooks = []

    for i in range(number_of_islands):
        logbook = tools.Logbook()
        logbook.header = ['gen', 'number_of_evaluations'] + (stats.fields if stats else [])

        logbooks.append(logbook)

    return logbooks, stats


def logs_do_nothing(toolbox: base.Toolbox) -> tools.Logbook:
    logbook = tools.Logbook()

    return logbook


def update_logs(toolbox: base.Toolbox, population: list, logs: tools.Logbook) -> tools.Logbook:
    return logs
