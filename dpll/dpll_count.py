from copy import copy

import fire
from pysat.formula import CNF

from dpll import dpll


class DPLLCount:
    def __init__(self, cnf_file=None, formula=None, choice_function=None):
        """
        Creates a DPLL search instance. Either the cnf_file or the formula must be supplied
        :param cnf_file: path to a .cnf file
        :param formula: pysat.formula.CNF instance
        :param choice_function: function that receives a formula (pysat.formula.CNF) and a model (dict(var->assignment in DIMACS notation)) and chooses the next literal to branch on
        """
        if cnf_file is None and formula is None:
            raise ValueError('Please provide either a cnf file or a formula')
        self.choose_literal = choice_function if choice_function is not None else dpll.choose_random_literal

        self.formula = formula if formula is not None else CNF(from_file=cnf_file)
        self.n_vars = formula.nv

        self.statistics = {
            'branches': 0,
            'unit_propagations': 0,
            'purifications': 0,
            'up_clauses_cleaned': 0,
            'up_literals_cleaned': 0,
        }

        self.solved = False
        self.model_count = 0

    def count(self):
        """
        Computes #SAT using the #DPLL algorithm and returns it.
        :return:
        """
        if not self.solved:
            self.model_count = self.__dpll_count(self.formula, {})
            self.solved = True
        return self.model_count

    def __dpll_count(self, f, model):
        """
        Runs the #DPLL algorithm on a given formula and a given (possibly partial)
        assignment (model)
        :param f: boolean formula (instance of pysat.formula.CNF)
        :param model: partial assignment (dict)
        :return:
        """
        # an empty formula is satisfiable (2^k solutions, k=#free variables)
        if len(f.clauses) == 0:
            return 2**len([free for free in range(1, self.n_vars+1) if free not in model])

        # if any clause is empty, the formula is UNSAT (0 solutions)
        if any([len(c) == 0 for c in f.clauses]):
            return 0

        # trying to use 'local' variables
        model = copy(model)
        f = f.copy()
        # print(partial_model_dict_to_list(f.nv, model))

        # unit propagation if f contains a unit clause
        l = dpll.find_unit_clause(f.clauses)
        if l is not None:
            model[abs(l)] = l  # adds the literal to its index in the model
            f = dpll.unit_propagation(f, l)
            return self.__dpll_count(f, model)

        # no unit propagations, must choose a literal to branch on
        l = self.choose_literal(f, model)

        # branches on asserted literal, collecting the number of models
        f.clauses.append([l])
        count = self.__dpll_count(f, model)
        # undoes last append and branches on negated literal
        del f.clauses[-1]
        f.clauses.append([-l])
        return count + self.__dpll_count(f, model)


def main(cnf_file):
    """
    Runs DPLL.solve in a given cnf_file
    :param cnf_file:
    :return:
    """
    solver = DPLLCount(cnf_file=cnf_file)
    return solver.count()
    # return ' '.join([str(x) for x in model_dict_to_list(f.nv, model)]) if model is not None else None


if __name__ == '__main__':
    fire.Fire(main)
