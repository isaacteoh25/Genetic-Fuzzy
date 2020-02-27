import sys, os
from copy import deepcopy
from random import randint, choice, random
import numpy as np
import re


class CNF:

    def __init__ (self, matrix: np.ndarray, count_variable: int, count_clause: int):
        self.matrix = matrix
        self.count_variable = count_variable
        self.count_clause = count_clause


def readCnf (cnfFile):
    problems = []
    cnfFile = open(cnfFile)
    problems.append(cnfFile.read())
    formulas = []
    for problem in problems:
        formula = parse(problem)
        formulas.append(formula)
    return formulas


def parse (dimacs: str):
    lines = dimacs.split('\n')
    line_offset = 0

    for line in lines:
        if line[0] == 'c':
            line_offset += 1
            continue

        if line[0] == 'p':
            line = line.strip(' ')
            line = re.sub(' +', ' ', line)
            line = line.split(' ')
            count_literals = int(line[2])
            count_clause = int(line[3])
            clauses = lines[line_offset + 1:]
            matrix = store_clause(clauses, count_clause)
            return CNF(matrix, count_literals, count_clause)


def store_clause (clauses_lines: list, count_clause: int):
    # 3CNF CNF as matrix where each vector is a clause
    matrix = np.zeros((count_clause, 3), np.int16)

    lines = ''.join(clauses_lines)
    lines = lines.replace('0%0', '')
    clause = re.split('[\t\n ]0|[\t\n ]0', lines)

    for clause_index, clause in enumerate(clause):
        clause = clause.strip(' ')
        literals = re.split('[\t\n ]', clause)

        for term_index, variable in enumerate(literals):
            represent = int(variable)
            matrix[clause_index, term_index] = represent

    return matrix

