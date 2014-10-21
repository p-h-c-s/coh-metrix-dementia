# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from os.path import dirname, abspath
from sys import modules


base_path = abspath(dirname(modules[__name__].__file__))


def ilen(it):
    """Calculate the number of elements in an iterable.
    """
    if isinstance(it, list) or isinstance(it, tuple):
        return len(it)

    count = 0
    for i in it:
        count = count + 1
    return count


def is_valid_id(string):
    """Check whether a string is a valid id.

    :string: The string to be checked
    :returns: True if the string represents a valid id; false otherwise.

    """
    import re

    return re.match("^[_A-Za-z][_a-zA-Z0-9]*$", string) is not None


# The following functions are used for counting the occurrences of operators
#   and connectives in a text.


def matches(candidate, operator, ignore_pos=False):
    """Check if candidate matches operator.

    :candidate: a token.
    :operator: an operator.
    :ignore_pos: whether or not to ignore the PoS tags.

    :returns: True if candidate matches operator; False otherwise.
    """
    if ignore_pos:
        return [w for w, _ in candidate] == [w for w, _ in operator]
    else:
        for token, oper in zip(candidate, operator):
            if type(oper[1]) is str:
                if token != oper:
                    return False
            elif type(oper[1]) is tuple:
                if token[0] != oper[0] or token[1] not in oper[1]:
                    return False
        return True


def count_occurrences(tagged_sent, operator, ignore_pos=False):
    """Count the number of occurrences of an operator in a tagged sentence.

    :tagged_sent: a tagged sentence.
    :operator: an operator.
    :ignore_pos: whether or not to ignore the PoS tags.

    :returns: The number of times the operator occurs in the sentence.
    """
    # 'tagged_sent' is like
    # [('O', 'ART'), ('gato', 'N'), ('sumiu', 'V'), ('.', 'PU')]
    # 'operator' is like
    # [('e', 'KC')]

    occurrences = 0
    for i, token in enumerate(tagged_sent):
        if token[0].lower() == operator[0][0]:
            candidate = [(w.lower(), t)
                         for w, t in tagged_sent[i:(i + len(operator))]]
            # print('can  ', candidate)
            if matches(candidate, operator, ignore_pos):
                occurrences += 1

    return occurrences


def count_occurrences_for_all(tagged_sent, operators, ignore_pos=False):
    """Count the total number of occurrences of a list of operators in a
    sentence.

    :tagged_sent: a tagged sentence.
    :operators: a list of operators.
    :ignore_pos: whether or not to ignore the PoS tags.

    :returns: The sum of the occurrences of each operator in the sentence.
    """
    return sum([count_occurrences(tagged_sent, operator, ignore_pos)
                for operator in operators])
