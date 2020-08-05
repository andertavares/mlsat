import unittest

import pysat

from dpll import dpll

N = 9
M = 3

def exactly_one(variables):
    cnf = [ variables ]
    n = len(variables)

    for i in range(n):
        for j in range(i+1, n):
            v1 = variables[i]
            v2 = variables[j]
            cnf.append([-v1, -v2])

    return cnf

def flatten_var(i, j, k):
    return i*N*N + j*N + k + 1

def unflatten_var(v):
    v, k = divmod(v-1, N)
    v, j = divmod(v, N)
    v, i = divmod(v, N)
    return i, j, k

def one_hot (cnf):
    for i in range(N):
        for j in range(N):
            cnf = cnf + exactly_one([ flatten_var(i,j,k) for k in range(N) ])
    return cnf

def row_rules (cnf):
    for j in range(N):
        for k in range(N):
            cnf = cnf + exactly_one([ flatten_var(i,j,k) for i in range(N) ])
    return cnf

def column_rules (cnf):
    for i in range(N):
        for k in range(N):
            cnf = cnf + exactly_one([ flatten_var(i,j,k) for j in range(N) ])
    return cnf

def region_rules (cnf):
    for k in range(N):
        for x in range(M):
            for y in range(M):
                v = [ flatten_var(y*M + i, x*M + j, k) for i in range(M) for j in range(M)]
                cnf = cnf + exactly_one(v)
    return cnf


class TestDPLL(unittest.TestCase):
    def test_sudoku(self):
        cnf = []

        cnf = cnf + one_hot(cnf)
        cnf = cnf + row_rules(cnf)
        cnf = cnf + column_rules(cnf)
        cnf = cnf + region_rules(cnf)

        #cnf = {frozenset(x) for x in cnf}
        #cnf = list(cnf)

        example = [
            (0, 0, 2),
            (0, 1, 5),
            (0, 4, 3),
            (0, 6, 9),
            (0, 8, 1),
            (1, 1, 1),
            (1, 5, 4),
            (2, 0, 4),
            (2, 2, 7),
            (2, 6, 2),
            (2, 8, 8),
            (3, 2, 5),
            (3, 3, 2),
            (4, 4, 9),
            (4, 5, 8),
            (4, 6, 1),
            (5, 1, 4),
            (5, 5, 3),
            (6, 3, 3),
            (6, 4, 6),
            (6, 7, 7),
            (6, 8, 2),
            (7, 1, 7),
            (7, 8, 3),
            (8, 0, 9),
            (8, 2, 3),
            (8, 6, 6),
            (8, 8, 4)
        ]

        cnf = cnf + [[flatten_var(z[0], z[1], z[2]) - 1] for z in example]
        f = pysat.formula.CNF(from_clauses=cnf)
        solution = dpll.model_dict_to_list(f.nv, dpll.dpll_solve(f, {}))

        X = [unflatten_var(v) for v in solution if v > 0]
        for i, cell in enumerate(sorted(X, key=lambda h: h[0] * N * N + h[1] * N)):
            print(cell[2] + 1, end=" ")
            if (i + 1) % N == 0: print("")


if __name__ == '__main__':
    unittest.main()
