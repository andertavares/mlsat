import unittest

import pysat

from dpll import dpll


class TestDPLL(unittest.TestCase):
    def test_choose_literal(self):
        pass

    def test_unit_propagation(self):
        f = pysat.formula.CNF(from_clauses=[[-1, -2], [2]])
        f = dpll.unit_propagation(f, 2)
        self.assertEqual([[-1]], f.clauses)

        f = dpll.unit_propagation(f, -1)
        self.assertEqual([], f.clauses)

    def test_dpll_solve_empty(self):
        f = pysat.formula.CNF(from_clauses=[])
        model = dpll.dpll_solve(f, {})
        self.assertIsNotNone(model)
        self.assertEqual({}, model)

    def test_dpll_solve_trivial_contradiction(self):
        f = pysat.formula.CNF(from_clauses=[[1], [-1]])
        self.assertIsNone(dpll.dpll_solve(f, {}))

    def test_dpll_solve_tautology(self):
        f = pysat.formula.CNF(from_clauses=[[1, -1]])
        model = dpll.dpll_solve(f, {})
        self.assertIsNotNone(model)
        # self.assertEqual({1: 1}, model)


if __name__ == '__main__':
    unittest.main()
