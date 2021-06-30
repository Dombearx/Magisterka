from abc import ABC

from evolalg.base.step import Step
import numpy as np


class Dissimilarity(Step, ABC):

    def __init__(self, reduction="mean", output_field="dissim", *args, **kwargs):
        super(Dissimilarity, self).__init__(*args, **kwargs)

        self.output_field = output_field
        self.fn_reduce = None
        if reduction == "mean":
            self.fn_reduce = np.mean
        elif reduction == "max":
            self.fn_reduce = np.max
        elif reduction == "min":
            self.fn_reduce = np.min
        elif reduction == "sum":
            self.fn_reduce = np.sum
        elif reduction == "none" or reduction == None:
            self.fn_reduce = None
        else:
            raise ValueError("Unknown reduction type. Supported: mean, max, min, sum, none")

    def reduce(self, dissim_matrix):
        if self.fn_reduce is None:
            return dissim_matrix
        return self.fn_reduce(dissim_matrix, axis=1)
