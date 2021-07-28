from deap import base
from operator import eq
from copy import deepcopy


class BasicParetoFront:

    def insert(self, item):
        item = deepcopy(item)

        self.items.append(item)
        self.keys.append(item.fitness)

    def remove(self, index):
        del self.keys[index]
        del self.items[index]

    def replace(self, index, item):
        item = deepcopy(item)

        self.keys[index] = item
        self.items[index] = item.fitness

    def update(self, population: list) -> list:
        return self.items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, i):
        return self.items[i]

    def __iter__(self):
        return iter(self.items)

    def __reversed__(self):
        return reversed(self.items)

    def __str__(self):
        return str(self.items)


class SimpleParetoFront(BasicParetoFront):

    def __init__(self, max_len, similar=eq):
        self.keys = list()
        self.items = list()
        self.max_len = max_len
        self.similar = similar

    def update(self, population):

        removed = 0

        for ind in population:
            is_dominated = False
            dominates_one = False
            has_twin = False
            to_remove = []
            for i, hofer in enumerate(self):  # hofer = hall of famer
                if not dominates_one and hofer.fitness.dominates(ind.fitness):
                    is_dominated = True
                    break
                elif ind.fitness.dominates(hofer.fitness):
                    dominates_one = True
                    to_remove.append(i)
                elif ind.fitness == hofer.fitness and self.similar(ind, hofer):
                    has_twin = True
                    break

            for i in reversed(to_remove):  # Remove the dominated hofer
                self.remove(i)
                removed += 1
            if not is_dominated and not has_twin:
                if len(self) < self.max_len:
                    self.insert(ind)

        return removed


def prepare_hall_of_fame(toolbox: base.Toolbox, size: int) -> SimpleParetoFront:
    return SimpleParetoFront(size)


def update_hall_of_fame(toolbox: base.Toolbox, population: list,
                        old_hall_of_fame: BasicParetoFront) -> BasicParetoFront:
    old_hall_of_fame.update(population)

    return old_hall_of_fame
