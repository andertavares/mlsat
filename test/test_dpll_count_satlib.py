import os
import shutil
import unittest
import tarfile

from pysat.solvers import Solver
from pysat.formula import CNF

from dpll.dpll_count import DPLLCount


class TestDPLLCount(unittest.TestCase):

    def test_count_sat20vars(self):
        """
        Tests the counter on 100 SATisfiable random 3CNFinstances with 20 vars
        (they were generated with cnfgen rather than from SATLIB)
        :return:
        """
        tmp_dir = '/tmp/sat100'
        with tarfile.open('instances/3cnf_v20_sat.tar.gz') as tf:
            tf.extractall(tmp_dir)
        for f in os.listdir(tmp_dir):
            print(f'Testing {f}')
            self.assertGreater(DPLLCount(cnf_file=os.path.join(tmp_dir, f)).count(), 0)
        shutil.rmtree(tmp_dir)

    def test_count_unsat20vars(self):
        """
        Tests the solver 100 UNSATisfiable random 3CNFinstances with 20 vars
        (they were generated with cnfgen rather than from SATLIB)
        :return:
        """
        tmp_dir = '/tmp/unsat100'
        with tarfile.open('instances/3cnf_v20_unsat.tar.gz') as tf:
            tf.extractall(tmp_dir)
        for f in os.listdir(tmp_dir):
            path = os.path.join(tmp_dir, f)
            with Solver(bootstrap_with=CNF(path).clauses) as s:
                count = len(list(s.enum_models()))
            self.assertEqual(count, DPLLCount(cnf_file=path).count())
        shutil.rmtree(tmp_dir)

    '''
    def test_dpll_solve_satlib_uf50_01(self):
        """
        Tests the solver on a SATisfiable instance from satlib
        :return:
        """
        # the following is a satisfiable assignment for 'uf50-01.cnf':
        # -1 2 -3 4 5 6 7 8 9 -10 -11 12 -13 14 15 -16 -17 -18 19 20 -21 -22 23 -24 -25
        # -26 27 -28 -29 -30 -31 32 -33 -34 35 36 37 38 39 -40 -41 -42 -43 -44 -45 -46
        # 47 48 49 -50
        f = CNF(from_file='instances/uf50-01.cnf')
        with Solver(bootstrap_with=f.clauses) as s:
            count = len(list(s.enum_models()))
        self.assertEqual(count, DPLLCount(cnf_file='instances/uf50-01.cnf').count())

    def test_dpll_solve_satlib_uuf50_01(self):
        """
        Tests the solver on a UNSATisfiable instance from satlib
        :return:
        """
        self.assertEqual(0, DPLLCount(cnf_file='instances/uuf50-01.cnf').count())

    def test_dpll_solve_satlib_uf50(self):
        """
        Tests the solver on the first 100 uf50 instances from satlib (all satisfiable)
        :return:
        """
        tmp_dir = '/tmp/uf50'
        with tarfile.open('instances/uf50-218_first100.tar.gz') as tf:
            tf.extractall(tmp_dir)
        for f in os.listdir(tmp_dir):
            print(f'Testing {f}')
            path = os.path.join(tmp_dir, f)
            with Solver(bootstrap_with=CNF(path).clauses) as s:
                count = len(list(s.enum_models()))
            self.assertEqual(count, DPLLCount(cnf_file=path).count())
        shutil.rmtree(tmp_dir)

    def test_dpll_solve_satlib_uuf50(self):
        """
        Tests the solver on the first 100 uuf50 instances from satlib (all UNsatisfiable)
        :return:
        """
        tmp_dir = '/tmp/uuf50'
        with tarfile.open('instances/uuf50-218_first100.tar.gz') as tf:
            tf.extractall(tmp_dir)
        for f in os.listdir(tmp_dir):
            print(f'Testing {f}')
            self.assertEqual(0, DPLLCount(cnf_file=os.path.join(tmp_dir, f)).count())
        shutil.rmtree(tmp_dir)
    '''

if __name__ == '__main__':
    unittest.main()
