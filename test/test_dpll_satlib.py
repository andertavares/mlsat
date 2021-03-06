import os
import shutil
import unittest
import tarfile

import pysat

from dpll import dpll


class TestDPLLSatlib(unittest.TestCase):

    def test_dpll_solve_satlib_uf50_01(self):
        """
        Tests the solver on a SATisfiable instance from satlib
        :return:
        """
        # the following is a satisfiable assignment for 'uf50-01.cnf':
        # -1 2 -3 4 5 6 7 8 9 -10 -11 12 -13 14 15 -16 -17 -18 19 20 -21 -22 23 -24 -25
        # -26 27 -28 -29 -30 -31 32 -33 -34 35 36 37 38 39 -40 -41 -42 -43 -44 -45 -46
        # 47 48 49 -50
        self.assertGreater(len(dpll.DPLL(cnf_file='instances/uf50-01.cnf').get_model_list()), 0)

    def test_dpll_solve_satlib_uf50_040(self):
        """
        Tests the solver on a SATisfiable instance from satlib
        that was problematic on the uf50 tests
        :return:
        """
        self.assertGreater(len(dpll.DPLL(cnf_file='instances/uf50-040_clean.cnf').get_model_list()), 0)

    def test_dpll_solve_satlib_uuf50_01(self):
        """
        Tests the solver on a UNSATisfiable instance from satlib
        :return:
        """
        self.assertEqual(0, len(dpll.DPLL(cnf_file='instances/uuf50-01.cnf').get_model_list()))

    def test_dpll_solve_sat20vars(self):
        """
        Tests the solver 100 SATisfiable random 3CNFinstances with 20 vars
        (they were generated with cnfgen rather than from SATLIB)
        :return:
        """
        tmp_dir = '/tmp/sat100'
        with tarfile.open('instances/3cnf_v20_sat.tar.gz') as tf:
            tf.extractall(tmp_dir)
        for f in os.listdir(tmp_dir):
            print(f'Testing {f}')
            model = dpll.DPLL(cnf_file=os.path.join(tmp_dir, f)).get_model_list()
            self.assertGreater(len(model), 0)
        shutil.rmtree(tmp_dir)

    def test_dpll_solve_unsat20vars(self):
        """
        Tests the solver 100 UNSATisfiable random 3CNFinstances with 20 vars
        (they were generated with cnfgen rather than from SATLIB)
        :return:
        """
        tmp_dir = '/tmp/unsat100'
        with tarfile.open('instances/3cnf_v20_unsat.tar.gz') as tf:
            tf.extractall(tmp_dir)
        for f in os.listdir(tmp_dir):
            print(f'Testing {f}')
            model = dpll.DPLL(cnf_file=os.path.join(tmp_dir, f)).get_model_list()
            self.assertEqual(len(model), 0)
        shutil.rmtree(tmp_dir)

    '''def test_dpll_solve_satlib_uf50(self):
        """
        Tests the solver on the first 100 uf50 instances from satlib (all satisfiable)
        :return:
        """
        tmp_dir = '/tmp/uf50'
        with tarfile.open('instances/uf50-218_first100.tar.gz') as tf:
            tf.extractall(tmp_dir)
        for f in os.listdir(tmp_dir):
            print(f'Testing {f}')
            model = dpll.DPLL(cnf_file=os.path.join(tmp_dir, f)).solve()
            print(model)
            self.assertGreater(len(model), 0)
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
            self.assertEqual(0, len(dpll.DPLL(cnf_file=os.path.join(tmp_dir, f)).get_model_list()))
        shutil.rmtree(tmp_dir)
    
    
    def test_dpll_solve_satlib_uf75(self):
        """
        Tests the solver on all uf75 instances from satlib (all satisfiable)
        :return:
        """
        tmp_dir = '/tmp/uf75'
        with tarfile.open('uf75-325.tar.gz') as tf:
            tf.extractall(tmp_dir)
        for f in os.listdir(tmp_dir):
            print(f'Testing {f}')
            self.assertNotEqual(0, len(dpll.DPLL(cnf_file=os.path.join(tmp_dir, f)).get_model_list()))
        shutil.rmtree(tmp_dir)

    def test_dpll_solve_satlib_uuf75(self):
        """
        Tests the solver on all uuf75 instances from satlib (all UNsatisfiable)
        :return:
        """
        tmp_dir = '/tmp/uuf75'
        with tarfile.open('uuf75-325.tar.gz') as tf:
            tf.extractall(tmp_dir)
        for f in os.listdir(tmp_dir):
            print(f'Testing {f}')
            self.assertEqual(0, len(dpll.DPLL(cnf_file=os.path.join(tmp_dir, f)).get_model_list()))
        shutil.rmtree(tmp_dir)
    '''


if __name__ == '__main__':
    unittest.main()
