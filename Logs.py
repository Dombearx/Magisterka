from deap import base


def logs_do_nothing(toolbox: base.Toolbox) -> list:
    return []


def update_logs(toolbox: base.Toolbox, population: list, logs: list) -> list:
    return logs
