from copy import copy, deepcopy
import itertools

import fire
from pysat.formula import CNF


class DPLL:
    def __init__(self, cnf_file=None, formula=None, choice_function=None):
        """
        Creates a DPLL search instances. Either the cnf_file or the formula must be supplied
        :param cnf_file: path to a .cnf file
        :param formula: pysat.formula.CNF instance
        :param choice_function: function that receives a formula (pysat.formula.CNF) and a model (dict(var->assignment in DIMACS notation)) and chooses the next literal to branch on
        """
        if cnf_file is None and formula is None:
            raise ValueError('Please provide either a cnf file or a formula')
        self.choose_literal = choice_function if choice_function is not None else choose_random_literal

        self.formula = formula if formula is not None else CNF(from_file=cnf_file)

        self.statistics = {
            'branches': 0,
            'unit_propagations': 0,
            'purifications': 0,
            'up_clauses_cleaned': 0,
            'up_literals_cleaned': 0,
        }

        self.solved = False
        self.model = None

    def solve(self):
        """
        Computes a solution using the DPLL algorithm and returns it.
        The solution is a dict(var -> value) in DIMACS notation and might
        a partial assignment of values to the variables.
        For example, {1: -1, 3: 3, 4: -4} means that x1=F, x2 is undetermined, x3=T, x4=F.
        Undetermined variables can be either T or F
        :return:
        """
        if not self.solved:
            self.model = self.__dpll(self.formula, {})
            self.solved = True
        return self.model

    def get_model_str(self):
        """
        Returns the computed solution as a space-separated string in DIMACS notation.
        Undetermined variables in the solution (see solve()) are assigned True.
        If the formula has no solution, returns an empty string
        :return:
        """
        self.solve()  # ensures that the solution has been computed
        return ' '.join([str(x) for x in self.get_model_list()])

    def get_model_list(self):
        """
        Returns the comptued solution as a list in DIMACS notation.
        Undetermined variables in the solution (see solve()) are assigned True.
        If the formula has no solution, returns an empty list.
        :return:
        """
        self.solve()
        return model_dict_to_list(self.formula.nv, self.model)

    def __dpll(self, f, model):
        """
        Runs the DPLL algorithm on a given formula and a given (possibly partial)
        assignment (model)
        Possible issue: model might have to be copied as partial assignments are not undone
        :param f: boolean formula (instance of pysat.formula.CNF)
        :param model: partial assignment (dict)
        :return:
        """
        # an empty formula is satisfiable
        if len(f.clauses) == 0:
            return model

        # if any clause is empty, the formula is UNSAT
        if any([len(c) == 0 for c in f.clauses]):
            return None

        # trying to use a 'local' variables
        model = copy(model)
        f = f.copy()
        # print(partial_model_dict_to_list(f.nv, model))

        # unit propagation if f contains a unit clause
        l = find_unit_clause(f.clauses)
        if l is not None:
            model[abs(l)] = l  # adds the literal to its index in the model
            f = unit_propagation(f, l)
            return self.__dpll(f, model)

        # purification: if f contains a literal with single polarity, set it up to provoke unit propagations
        l = find_single_polarity(f.clauses)
        if l is not None:
            # adds a unit clause with l to f to trigger unit propagation
            f.clauses.append([l])
            return self.__dpll(f, model)

        # no unit propagations or pure literals, must choose a literal to branch on
        l = self.choose_literal(f, model)

        # tries to branch on asserted then on negated literal
        f.clauses.append([l])
        result = self.__dpll(f, model)
        if result is not None:
            return result
        else:
            # undoes last append and insert negated literal
            del f.clauses[-1]
            f.clauses.append([-l])
            return self.__dpll(f, model)


def check_model(clauses, model):
    """
    Returns whether an assignment (model) satisfies the clauses
    :param clauses: list of lists, where each inner list contains positive or negated literals
    :param model: list, where each element is a variable asserted (positive value) or negated (negative value)
    :return:
    """
    # in all clauses, there must be at least one literal that agrees on sign with
    # its assignment in the model
    return all([any([model[abs(l) - 1] * l > 0 for l in clause]) for clause in clauses])


def model_dict_to_list(nvars, model):
    """
    Converts a dict with the assignments of a formula to a simple list (0-based indexing)
    Free variables are assigned positive literals
    :param nvars: number of variables in the formula (required to verify free literals)
    :param model:
    :return:
    """
    # returns an empty list if the model is none
    if model is None:
        return []
    # if v is a free variable in the model, it is absent in the dict and get returns it asserted to the list
    model_list = [model.get(v, v) for v in range(1, nvars+1)]

    return model_list


def partial_model_dict_to_list(nvars, model):
    """
    Converts a dict with the assignments of a formula to a simple list (0-based indexing)
    Free variables appear as 0
    :param nvars: number of variables in the formula (required to verify free literals)
    :param model:
    :return:
    """
    # if v is a free variable in the model, it is absent in the dict and get returns 0 to indicate it
    model_list = [model.get(v, 0) for v in range(1, nvars+1)]

    return model_list


def choose_random_literal(f, model):
    """
    Chooses a free literal at random
    :param f: an instance of pysat.formula.CNF
    :param model:
    :return:
    """
    import random

    # adds a positive and a negative literal for each variable not yet assigned
    free_literals = [v for v in range(1, f.nv+1) if v not in model]
    free_literals += [-v for v in range(1, f.nv+1) if v not in model]
    return random.choice(free_literals)


def unit_propagation(f, l):
    """
    Performs unit propagation of literal l in formula f.
    That is, removes all clauses with l and removes ~l from the clauses it occurs
    :param f:
    :param l:
    :return:
    """
    new_f = f.copy()
    # removes clauses with l
    occurrences = [l not in c for c in f.clauses]   # creates an array mask to keep clauses without l
    new_f.clauses = list(itertools.compress(f.clauses, occurrences))  # filters the old list with the mask

    # removes occurrences of ~l
    for c in new_f.clauses:
        # python triggers ValueError if the element is not on the list
        try:
            c.remove(-l)
        except ValueError:
            pass  # ignore the error

    return new_f


def find_single_polarity(clauses):
    """
    Returns one literal that occurs with a single polarity
    in the formula, or None if none is found
    :param clauses:
    :return:
    """
    # construct a set with all literals
    literals = set()
    for c in clauses:
        literals = literals.union({lit for lit in c})

    # returns the first literal whose negated is not present (i.e. a pure literal)
    for lit in literals:
        if -lit not in literals:
            return lit
    return None


def find_unit_clause(clauses):
    """
    Returns the literal of the first unit clause found
    Returns None if there are no unit clauses
    :param clauses:
    :return:
    """
    for c in clauses:
        if len(c) == 1:
            return c[0]
    return None


def main(cnf_file):
    """
    Runs DPLL.solve in a given cnf_file
    :param cnf_file:
    :return:
    """
    solver = DPLL(cnf_file=cnf_file)
    return solver.solve()
    # return ' '.join([str(x) for x in model_dict_to_list(f.nv, model)]) if model is not None else None


if __name__ == '__main__':
    fire.Fire(main)
