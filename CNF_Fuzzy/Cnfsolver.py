import Genetic
import json
import os
import time
from json import JSONEncoder


class Cnfsolver:

    def __init__ (self, formulas):
        self.formulas = formulas

    def solver (self):

        global solution

        metrics_dict = {}
        for formula in self.formulas:
            solve = Genetic.Genetic(formula)
            solution, generation = solve.solve()

            count_variable = formula.count_variable

            if count_variable in metrics_dict:
                metrics = metrics_dict[count_variable]
            else:
                metrics = Metrics(count_variable)
                metrics_dict[count_variable] = metrics

            if solution is not None:
                metrics.count_success += 1


            else:
                metrics.count_failure += 1

        success_rate = 0
        for count_variable in metrics_dict.keys():
            metrics = metrics_dict[count_variable]

            experiments = metrics.count_success + metrics.count_failure

            if experiments:
                success_rate = metrics.count_success / (metrics.count_success + metrics.count_failure)

        return success_rate, solution, generation


class Metrics:

    def __init__ (self, count_variable):
        self.count_variable = count_variable
        self.count_success = 0
        self.count_failure = 0
