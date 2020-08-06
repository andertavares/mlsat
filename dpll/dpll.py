from pysat.formula import CNF
import itertools
import fire


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
    :param nvars: number of variables in the formula (required to verify free literals)
    :param model:
    :return:
    """
    # if v is a free variable in the model, it be absent in the dict and get returns it asserted to the list
    model_list = [model.get(v, v) for v in range(1, nvars+1)]

    return model_list


def dpll(cnf_file):
    """
    Runs dpll_solve in a given cnf_file
    :param cnf_file:
    :return:
    """
    f = CNF(from_file=cnf_file)
    return dpll_solve(f, {})


def dpll_solve(f, model):
    """
    Runs the DPLL algorithm on a given formula and a given partial
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

    # unit propagation if f contains a unit clause
    l = find_unit_clause(f.clauses)
    if l is not None:
        model[abs(l)] = l  # adds the literal to its index in the model
        f = unit_propagation(f, l)
        return dpll_solve(f, model)

    # purification: if f contains a literal with single polarity, set it up to provoke unit propagations
    l = find_single_polarity(f.clauses)
    if l is not None:
        # adds a unit clause with l to f to trigger unit propagation
        f.clauses.append([l])
        return dpll_solve(f, model)

    # no unit propagations or pure literals, must choose a literal to branch on
    l = choose_literal(f, model)
    # adds a unit clause with l to f to trigger unit propagation
    f.clauses.append([l])
    return dpll_solve(f, model)


def choose_literal(f, model):
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


if __name__ == '__main__':
    fire.Fire(dpll)
