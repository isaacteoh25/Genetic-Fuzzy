import math
import numpy as np
import random
from Fuzzy import Fuzzy


class Genetic:
    popSize = 20
    prop_limit = 0
    iteration_limit = 1500
    fitnessFuzzy = []

    def __init__ (self, formula):
        self.formula = formula
        self.pop = np.zeros((Genetic.popSize, formula.count_variable), np.bool)
        self.iteration = 0
        # self.AD = 0

        count_variable = formula.count_variable

        for i in range(1, Genetic.popSize + 1):
            countT = int(((2 * i * count_variable) - count_variable) / (2 * Genetic.popSize))

            for j in range(0, countT):
                self.pop[i - 1, j] = True

        self.pop.transpose()
        np.random.shuffle(self.pop)
        self.pop.transpose()

    def solve (self):

        pop_results = []
        num_generations = 1500
        # while True:
        for generation in range(num_generations):

            # if self.iteration > Genetic.iteration_limit:
            #     return None

            for i in range(0, Genetic.popSize):
                # if self.iteration > Genetic.iteration_limit:
                #     return None

                fit = self.fitness_function(self.pop[i, :])

                if fit == self.formula.count_clause:
                    solution = self.pop[i, :]
                    return solution, generation

                # pre_fuzzy = fit / self.formula.count_clause
                result = Evaluate(fit, i)
                # nn.train([fit], [self.formula.count_clause])
                pop_results.append(result)
                # fuzzy_results=pop_results
            pop_results.sort(key=lambda res: res.fitness, reverse=True)

            if not self.offspring_production(pop_results, generation):
                return None

            # self.iteration += 1

    def fitness_function (self, literal_instance: np.array):

        count_satisfy = 0

        for idx_clause in range(0, self.formula.count_clause):
            for idx_term in range(0, 3):

                literal = self.formula.matrix[idx_clause, idx_term]
                true_value = literal_instance[abs(literal) - 1]

                if literal < 0:
                    true_value = not true_value

                if true_value:
                    count_satisfy += 1
                    break

        return count_satisfy

    def offspring_production (self, pop_results, generation):

        disrupt_rate = 0.1
        fitness_sum = sum(r.fitness for r in pop_results[Genetic.prop_limit:])
        parents = []
        distance = []
        evo_sys = 0
        avg_div = 0
        AD = 0
        Genetic.fitnessFuzzy.append((fitness_sum / self.formula.count_clause) / Genetic.popSize)
        if generation > 0:
            evo_sys = (Genetic.fitnessFuzzy[generation] - Genetic.fitnessFuzzy[generation - 1]) / Genetic.fitnessFuzzy[
                generation - 1]
            for i in range(Genetic.prop_limit, Genetic.popSize - 1):
                for j in range(0, self.formula.count_variable):
                    x = self.pop[i, math.ceil(self.formula.count_variable / 2)]
                    x = int(x == 'true')
                    y = self.pop[i, j]
                    y = int(y == 'true')
                    distance.append((x - y))
                AD += (distance[i] * distance[i])
            avg_div = math.sqrt(AD) / Genetic.popSize
            fuzzy = Fuzzy(avg_div, evo_sys)
            disrupt_rate = fuzzy.fuzzy_output()
        for n in range(Genetic.prop_limit, Genetic.popSize):
            # if self.iteration > Genetic.iteration_limit:
            #     return False

            selected_index = self.parent_selection(pop_results, fitness_sum)
            parents.append(selected_index)

        for i in range(Genetic.prop_limit, Genetic.popSize - 1):

            mutate = random.random() >= (1 - disrupt_rate)

            for j in range(0, self.formula.count_variable):
                # if self.iteration > Genetic.iteration_limit:
                #     return False
                self.generational(i, j, mutate, parents)

            if not self.flip_heuristic(i):
                return False

            return True

    def generational (self, i, j, mutate, parents):
        flip = random.getrandbits(1)
        if random.getrandbits(1):
            parent_index = parents[i - Genetic.prop_limit]
            self.pop[i, j] = self.pop[parent_index, j]
        else:
            parent_index = parents[i + 1 - Genetic.prop_limit]
            self.pop[i, j] = self.pop[parent_index, j]

            if mutate & flip:
                self.pop[i, j] = not self.pop[i, j]

    def flip_heuristic (self, pop_index):

        initial_fitness = self.fitness_function(self.pop[pop_index, :])
        post_fitness = initial_fitness

        while True:
            order = np.arange(self.formula.count_variable)
            np.random.shuffle(order)
            for index in order:

                # if self.iteration > Genetic.iteration_limit:
                #     return False

                pre_fitness = self.fitness_function(self.pop[pop_index, :])
                self.pop[pop_index, index] = not self.pop[pop_index, index]
                post_fitness = self.fitness_function(self.pop[pop_index, :])

                gain = post_fitness - pre_fitness

                if gain < 0:
                    self.pop[pop_index, index] = not self.pop[pop_index, index]

            if post_fitness <= initial_fitness:
                return True

            initial_fitness = post_fitness

    @staticmethod
    def parent_selection (pop_results, fitness_sum):
        select_prob = random.random()
        cum_prob = 0.0
        for result in pop_results[Genetic.prop_limit:]:
            cum_prob += result.fitness / fitness_sum
            if select_prob <= cum_prob:
                return result.index_pop


class Evaluate:
    def __init__ (self, fit, index_pop):
        self.fitness = fit
        self.index_pop = index_pop
