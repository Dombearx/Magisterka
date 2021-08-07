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


class ApproximateParetoFront(BasicParetoFront):

    def __init__(self, max_len, precisions, similar=eq):
        self.keys = list()
        self.items = list()
        self.max_len = max_len
        self.similar = similar
        self.precisions = precisions

    def is_same(self, hofer, other, precisions):
        for v1, v2, prec in zip(hofer.fitness.wvalues, other.fitness.wvalues, precisions):
            if round(v1, prec) != round(v2, prec):
                return False

        return True

    def dominates_with_precision(self, other, hofer, precisions):
        for v1, v2, prec in zip(other.fitness.wvalues, hofer.fitness.wvalues, precisions):
            if round(v1, prec) < round(v2, prec):
                return False

        return True

    def update(self, population):

        removed = 0


        for ind in population:
            to_remove = []
            # print("testing", ind.fitness)
            has_twin = False
            dominates_one = False
            is_dominated = False
            for i, hofer in enumerate(self):
                if self.is_same(hofer, ind, self.precisions):
                    has_twin = True
                    break
                if self.dominates_with_precision(ind, hofer, self.precisions):
                    to_remove.append(i)
                    dominates_one = True
                if not dominates_one and self.dominates_with_precision(hofer, ind, self.precisions):
                    is_dominated = True
                    break

            for i in reversed(to_remove):  # Remove the dominated hofer
                # print("removing", i, self, has_twin, dominates_one, is_dominated)
                self.remove(i)
                removed += 1
            if not is_dominated and not has_twin:
                if len(self) < self.max_len:
                    self.insert(ind)

        return removed


def prepare_hall_of_fame(toolbox: base.Toolbox, size: int) -> SimpleParetoFront:
    return SimpleParetoFront(size)

def prepare_precision_hall_of_fame(toolbox: base.Toolbox, size: int, precisions: list) -> ApproximateParetoFront:
    return ApproximateParetoFront(size, precisions)

def update_hall_of_fame(toolbox: base.Toolbox, population: list,
                        old_hall_of_fame: BasicParetoFront) -> (BasicParetoFront, list):
    removed_individuals = 0
    for island in population:
        removed_individuals += old_hall_of_fame.update(island)
    return old_hall_of_fame, removed_individuals
