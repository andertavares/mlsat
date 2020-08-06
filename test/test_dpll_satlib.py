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
        self.assertIsNotNone(dpll.dpll('uf50-01.cnf'))

    def test_dpll_solve_satlib_uuf50_01(self):
        """
        Tests the solver on a UNSATisfiable instance from satlib
        :return:
        """
        self.assertIsNone(dpll.dpll('uuf50-01.cnf'))

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
            self.assertIsNotNone(dpll.dpll(os.path.join(tmp_dir, f)))
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
            self.assertIsNone(dpll.dpll(os.path.join(tmp_dir, f)))
        shutil.rmtree(tmp_dir)


if __name__ == '__main__':
    unittest.main()
