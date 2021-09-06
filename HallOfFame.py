from deap import base
from deap.benchmarks import tools
from operator import eq
from copy import deepcopy
import pprint as pp
from deap.tools import ParetoFront
from bisect import bisect_right
import numpy as np


class DeapHallOfFame(object):
    """The hall of fame contains the best individual that ever lived in the
    population during the evolution. It is lexicographically sorted at all
    time so that the first element of the hall of fame is the individual that
    has the best first fitness value ever seen, according to the weights
    provided to the fitness at creation time.

    The insertion is made so that old individuals have priority on new
    individuals. A single copy of each individual is kept at all time, the
    equivalence between two individuals is made by the operator passed to the
    *similar* argument.

    :param maxsize: The maximum number of individual to keep in the hall of
                    fame.
    :param similar: An equivalence operator between two individuals, optional.
                    It defaults to operator :func:`operator.eq`.

    The class :class:`HallOfFame` provides an interface similar to a list
    (without being one completely). It is possible to retrieve its length, to
    iterate on it forward and backward and to get an item or a slice from it.
    """
    def __init__(self, maxsize, similar=eq):
        self.maxsize = maxsize
        self.keys = list()
        self.items = list()
        self.similar = similar

    def update(self, population):
        """Update the hall of fame with the *population* by replacing the
        worst individuals in it by the best individuals present in
        *population* (if they are better). The size of the hall of fame is
        kept constant.

        :param population: A list of individual with a fitness attribute to
                           update the hall of fame with.
        """
        removed = 0
        for ind in population:
            if len(self) == 0 and self.maxsize != 0:
                # Working on an empty hall of fame is problematic for the
                # "for else"
                self.insert(population[0])
                continue
            if ind.fitness > self[-1].fitness or len(self) < self.maxsize:
                for hofer in self:
                    # Loop through the hall of fame to check for any
                    # similar individual
                    if self.similar(ind, hofer):
                        break
                else:
                    # The individual is unique and strictly better than
                    # the worst
                    if len(self) >= self.maxsize:
                        self.remove(-1)
                        removed += 1
                    self.insert(ind)

        return removed

    def get_best_individual_fitness(self):

        if len(self) == 0:
            return "Empty hall of fame"

        return self[0].fitness.values

    def insert(self, item):
        """Insert a new individual in the hall of fame using the
        :func:`~bisect.bisect_right` function. The inserted individual is
        inserted on the right side of an equal individual. Inserting a new
        individual in the hall of fame also preserve the hall of fame's order.
        This method **does not** check for the size of the hall of fame, in a
        way that inserting a new individual in a full hall of fame will not
        remove the worst individual to maintain a constant size.

        :param item: The individual with a fitness attribute to insert in the
                     hall of fame.
        """
        item = deepcopy(item)
        i = bisect_right(self.keys, item.fitness)
        self.items.insert(len(self) - i, item)
        self.keys.insert(i, item.fitness)

    def remove(self, index):
        """Remove the specified *index* from the hall of fame.

        :param index: An integer giving which item to remove.
        """
        del self.keys[len(self) - (index % len(self) + 1)]
        del self.items[index]

    def clear(self):
        """Clear the hall of fame."""
        del self.items[:]
        del self.keys[:]

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


class InfiniteParetoFront(ParetoFront):
    def __init__(self, similar=eq):
        ParetoFront.__init__(self, similar)


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

    def update(self, population: list, toolbox) -> list:
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


class NSGA2ParetoFront(BasicParetoFront):
    def __init__(self, max_len, similar=eq):
        self.keys = list()
        self.items = list()
        self.max_len = max_len
        self.similar = similar

    def update(self, population, toolbox):

        old = deepcopy(self.items)

        removed = 0

        # for ind in population:
        #     dominates_one = False
        #     to_remove = []
        #     for i, hofer in enumerate(self):  # hofer = hall of famer
        #         if not dominates_one and hofer.fitness.dominates(ind.fitness):
        #
        #             break
        #         elif ind.fitness.dominates(hofer.fitness):
        #             dominates_one = True
        #             to_remove.append(i)
        #         elif ind.fitness == hofer.fitness and self.similar(ind, hofer):
        #             break
        #
        #     removed += len(to_remove)

        new = toolbox.select(self.items + population, min(self.max_len, len(self.items) + len(population)))

        vals = [ind.fitness.values for ind in new + old]

        vals = np.array(vals)

        ref = np.max(vals, axis=0)

        if len(old) > 0:
            old_hv = tools.hypervolume(old, ref)
        else:
            old_hv = float("-inf")
        new_hv = tools.hypervolume(new, ref)

        if new_hv > old_hv or not old:
            # print("better hall of fame: ", new_hv)
            self.items = new

            self.keys = []
            for item in self.items:
                self.keys.append(item.fitness)

        for item in old:
            if item not in self.items:
                removed += 1

        # pp.pprint([o.fitness for o in old])
        # print("-------- ", removed)
        # pp.pprint([o.fitness for o in self.items])
        # print("============")
        # x = input()

        return removed

    def get_best_individual_fitness(self):

        if len(self) == 0:
            return "Empty hall of fame"

        return min([ind.fitness.values for ind in self])


class SimpleParetoFront(BasicParetoFront):

    def __init__(self, max_len, similar=eq):
        self.keys = list()
        self.items = list()
        self.max_len = max_len
        self.similar = similar

    def update(self, population, toolbox):

        removed = 0

        for ind in population:
            if len(self) == 0 and self.max_len != 0:
                # Working on an empty hall of fame is problematic for the
                # "for else"
                self.insert(ind)
                continue
            if ind.fitness > self[-1].fitness or len(self) < self.max_len:
                for hofer in self:
                    # Loop through the hall of fame to check for any
                    # similar individual
                    if self.similar(ind, hofer):
                        break
                else:
                    # The individual is unique and strictly better than
                    # the worst
                    if len(self) >= self.max_len:
                        self.remove(-1)
                        removed += 1
                    self.insert(ind)

        # print(self[0].fitness.values)
        # for ind in population:
        #     is_dominated = False
        #     dominates_one = False
        #     has_twin = False
        #     to_remove = []
        #     for i, hofer in enumerate(self):  # hofer = hall of famer
        #         if not dominates_one and hofer.fitness.dominates(ind.fitness):
        #             is_dominated = True
        #             break
        #         elif ind.fitness.dominates(hofer.fitness):
        #             dominates_one = True
        #             to_remove.append(i)
        #         elif ind.fitness == hofer.fitness and self.similar(ind, hofer):
        #             has_twin = True
        #             break
        #
        #     for i in reversed(to_remove):  # Remove the dominated hofer
        #         self.remove(i)
        #         removed += 1
        #     if not is_dominated and not has_twin:
        #         if len(self) < self.max_len:
        #             self.insert(ind)

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

    def update(self, population, toolbox):

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


def prepare_NSGA2_hall_of_fame(toolbox: base.Toolbox, size: int) -> NSGA2ParetoFront:
    return NSGA2ParetoFront(size)


def prepare_Inifite_hall_of_fame(toolbox: base.Toolbox) -> InfiniteParetoFront:
    return InfiniteParetoFront()


def update_infinite_hall_of_fame(toolbox: base.Toolbox, population: list,
                                 old_hall_of_fame: InfiniteParetoFront) -> int:
    removed_individuals = 0
    for island in population:
        old_hall_of_fame.update(island)
    return removed_individuals


def prepare_DEAP_hall_of_fame(toolbox: base.Toolbox, size: int) -> DeapHallOfFame:
    return DeapHallOfFame(size)


def update_DEAP_hall_of_fame(toolbox: base.Toolbox, population: list,
                             old_hall_of_fame: DeapHallOfFame) -> int:
    removed_individuals = 0
    for island in population:
        removed_individuals += old_hall_of_fame.update(island)
    return removed_individuals


def prepare_precision_hall_of_fame(toolbox: base.Toolbox, size: int, precisions: list) -> ApproximateParetoFront:
    return ApproximateParetoFront(size, precisions)


def update_hall_of_fame(toolbox: base.Toolbox, population: list,
                        old_hall_of_fame: BasicParetoFront) -> int:
    removed_individuals = 0
    for island in population:
        removed_individuals += old_hall_of_fame.update(island, toolbox)
    return removed_individuals
