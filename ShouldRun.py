def n_iters_run(removed_individuals: int, iter_num: int, max_iters: int) -> bool:
    return iter_num < max_iters


iters_without_improvement = 0


def n_iters_without_improvement(removed_individuals: int, iter_num: int, max_iters: int) -> bool:
    global iters_without_improvement

    if removed_individuals == 0:
        iters_without_improvement += 1
    else:
        iters_without_improvement = 0

    if iters_without_improvement > max_iters:
        iters_without_improvement = 0
        return False

    return True
