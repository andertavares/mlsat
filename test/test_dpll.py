import os
import unittest
import tarfile

import pysat

from dpll import dpll


class TestDPLL(unittest.TestCase):
    def test_check_model(self):
        # basic test
        self.assertTrue(dpll.check_model([[1, -2], [2]], [1, 2]))
        self.assertFalse(dpll.check_model([[1, -2], [2]], [1, -2]))
        self.assertFalse(dpll.check_model([[1, -2], [-2]], [1, 2]))

        # testing a tautology
        taut = [[1, -1], [2, -2]]
        self.assertTrue(dpll.check_model(taut, [-1, -2]))
        self.assertTrue(dpll.check_model(taut, [-1, 2]))
        self.assertTrue(dpll.check_model(taut, [1, -2]))
        self.assertTrue(dpll.check_model(taut, [1, 2]))

        # testing a contradiction
        unsat = [[1, 2], [-1, -2], [-1, 2], [1, -2]]
        self.assertFalse(dpll.check_model(unsat, [-1, -2]))
        self.assertFalse(dpll.check_model(unsat, [-1, 2]))
        self.assertFalse(dpll.check_model(unsat, [1, -2]))
        self.assertFalse(dpll.check_model(unsat, [1, 2]))

        # testing uf75-044_clean.cnf, 1st model calculated with picosat, 2nd with our dpll :)
        model = [1, 2, 3, 4, -5, -6, -7, -8, -9, -10, -11, 12, -13, 14, -15, -16, -17, 18, -19, -20, -21, -22, 23, -24, 25, 26, 27, 28, -29, -30, -31, -32, 33, 34, 35, 36, -37, 38, -39, 40, -41, 42, -43, -44, -45, -46, -47, -48, 49, -50, 51, 52, 53, 54, 55, -56, 57, -58, -59, 60, 61, -62, -63, 64, -65, 66, 67, 68, -69, -70, -71, -72, 73, 74, 75]
        # model = [1, 2, 3, 4, -5, -6, -7, -8, -9, -10, -11, 12, -13, 14, -15, -16, -17, 18, -19, -20, -21, -22, 23, -24, 25, 26, 27, 28, -29, -30, -31, -32, 33, 34, 35, 36, -37, 38, -39, 40, -41, 42, -43, -44, 45, -46, -47, -48, 49, -50, 51, 52, 53, 54, 55, -56, -57, -58, -59, 60, 61, -62, -63, 64, -65, 66, 67, 68, -69, -70, -71, -72, 73, -74, 75]
        f = pysat.formula.CNF('uf75-044_clean.cnf')
        self.assertTrue(dpll.check_model(f.clauses, model))

    def test_model_dict_to_list(self):
        self.assertEqual([1, 2, -3], dpll.model_dict_to_list(3, {1: 1, 3: -3}))
        self.assertEqual([-1, 2, 3], dpll.model_dict_to_list(3, {1: -1}))
        self.assertEqual([-1, 2, 3, -4, 5], dpll.model_dict_to_list(5, {1: -1, 4: -4}))
        self.assertEqual([], dpll.model_dict_to_list(5, {}))

    def test_find_single_polarity(self):
        self.assertEqual(1, dpll.find_single_polarity([[1, -2], [2]]))
        self.assertEqual(1, dpll.find_single_polarity([[1, -2], [1]]))
        self.assertEqual(-2, dpll.find_single_polarity([[1, -2], [-1]]))
        self.assertEqual(-2, dpll.find_single_polarity([[1, -2], [-1, -2]]))
        self.assertEqual(None, dpll.find_single_polarity([[1, -2], [-1, 2]]))

    def test_find_unit_clause(self):
        self.assertEqual(2, dpll.find_unit_clause([[1, -2], [2]]))
        self.assertEqual(-1, dpll.find_unit_clause([[1, -2], [-1]]))
        self.assertEqual(None, dpll.find_unit_clause([[1, -2], [-1, 2]]))

    def test_unit_propagation_until_empty(self):
        f = pysat.formula.CNF(from_clauses=[[-1, -2], [2]])
        f = dpll.unit_propagation(f, 2)
        self.assertEqual([[-1]], f.clauses)

        f = dpll.unit_propagation(f, -1)
        self.assertEqual([], f.clauses)

    def test_unit_propagation_multiple_clauses_removed(self):
        f = pysat.formula.CNF(from_clauses=[[-1, -2], [2], [2, -3, -4]])
        f = dpll.unit_propagation(f, 2)
        self.assertEqual([[-1]], f.clauses)

    def test_dpll_solve_empty(self):
        f = pysat.formula.CNF(from_clauses=[])
        model = dpll.DPLL(formula=f).solve()
        self.assertIsNotNone(model)
        self.assertEqual({}, model)

    def test_dpll_solve_trivial_contradiction(self):
        f = pysat.formula.CNF(from_clauses=[[1], [-1]])
        solver = dpll.DPLL(formula=f)
        model = solver.solve()
        self.assertIsNone(model)

    def test_dpll_solve_tautology(self):
        f = pysat.formula.CNF(from_clauses=[[1, -1]])
        model = dpll.DPLL(formula=f).solve()
        self.assertIsNotNone(model)

    def test_dpll_solve_with_pure_literals(self):
        f = pysat.formula.CNF(from_clauses=[[1, -2], [1, 3], [-3, -2]])
        model = dpll.DPLL(formula=f).solve()
        self.assertIsNotNone(model)
        self.assertEqual({1: 1, 3: -3}, model)

    def test_get_model_list(self):
        """
        Same test as before, plus get_model_list
        :return:
        """
        f = pysat.formula.CNF(from_clauses=[[1, -2], [1, 3], [-3, -2]])
        solver = dpll.DPLL(formula=f)
        model = solver.solve()
        self.assertIsNotNone(model)
        self.assertEqual({1: 1, 3: -3}, model)
        self.assertEqual([1, 2, -3], solver.get_model_list())

    def test_get_model_str(self):
        """
        Same test as before, plus get_model_str
        :return:
        """
        f = pysat.formula.CNF(from_clauses=[[1, -2], [1, 3], [-3, -2]])
        solver = dpll.DPLL(formula=f)
        model = solver.solve()
        self.assertIsNotNone(model)
        self.assertEqual({1: 1, 3: -3}, model)
        self.assertEqual('1 2 -3', solver.get_model_str())



if __name__ == '__main__':
    unittest.main()
