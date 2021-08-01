def n_iters_run(removed_individuals: int, iter_num: int, max_iters: int) -> bool:
    return iter_num < max_iters


class NItersWithoutImprovement:
    def __init__(self):

        self.iters_without_improvement = 0

    def n_iters_without_improvement(self, removed_individuals: int, iter_num: int, max_iters: int) -> bool:

        if removed_individuals == 0:
            self.iters_without_improvement += 1

        if self.iters_without_improvement > max_iters:
            return False

        return True
