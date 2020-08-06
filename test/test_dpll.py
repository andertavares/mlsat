import unittest

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

    def test_model_dict_to_list(self):
        self.assertEqual([1, 2, -3], dpll.model_dict_to_list(3, {1: 1, 3: -3}))
        self.assertEqual([-1, 2, 3], dpll.model_dict_to_list(3, {1: -1}))
        self.assertEqual([-1, 2, 3, -4, 5], dpll.model_dict_to_list(5, {1: -1, 4: -4}))

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

    def test_dpll_solve_with_pure_literals(self):
        f = pysat.formula.CNF(from_clauses=[[1, -2], [1, 3], [-3, -2]])
        model = dpll.dpll_solve(f, {})
        self.assertIsNotNone(model)
        self.assertEqual({1: 1, 3: -3}, model)

    def test_dpll_solve_satlib_uf(self):
        """
        Tests the solver on a SATisfiable instance from satlib
        :return:
        """
        # the following is a satisfiable assignment for 'uf50-01.cnf':
        # -1 2 -3 4 5 6 7 8 9 -10 -11 12 -13 14 15 -16 -17 -18 19 20 -21 -22 23 -24 -25
        # -26 27 -28 -29 -30 -31 32 -33 -34 35 36 37 38 39 -40 -41 -42 -43 -44 -45 -46
        # 47 48 49 -50
        self.assertIsNotNone(dpll.dpll('uf50-01.cnf'))

    def test_dpll_solve_satlib_uuf(self):
        """
        Tests the solver on a UNSATisfiable instance from satlib
        :return:
        """
        self.assertIsNone(dpll.dpll('uuf50-01.cnf'))


if __name__ == '__main__':
    unittest.main()
