# -*- coding: utf-8 -*-
from coh import base
from coh.resource_pool import rp as default_rp
from coh.utils import base_path


LOGIC_OPERATORS = [
    [('e', 'KC')],
    [('ou', 'KC')],
    [('se', 'KS')],
    [('não', 'ADV')],
    [('nem', 'KC')],
    [('nenhum', ('PROAJD', 'PROSUB'))],
    [('nenhuma', ('PROADJ', 'PROSUB'))],
    [('nada', ('PROADJ', 'PROSUB'))],
    [('nunca', 'ADV')],
    [('jamais', 'ADV')],
    [('caso', 'KS')],
    [('desde', 'KS'), ('que', 'KS')],
    [('contanto', 'KS'), ('que', 'KS')],
    [('uma', 'KS'), ('vez', 'KS'), ('que', 'KS')],
    [('a', 'KS'), ('menos', 'KS'), ('que', 'KS')],
    [('sem', 'KS'), ('que', 'KS')],
    [('a', 'KS'), ('não', 'KS'), ('ser', 'KS'), ('que', 'KS')],
    [('salvo', 'KS'), ('se', 'KS')],
    [('exceto', 'KS'), ('se', 'KS')],
    [('então', 'KS'), ('é', 'KS'), ('porque', 'KS')],
    [('fosse...fosse', '??')],  # TODO: check how to handle this.
    [('vai', 'KS'), ('que', 'KS')],
    [('va', 'KS'), ('que', 'KS')],
]

NEGATIONS = [
    [('não', 'ADV')],
    [('nem', 'KC')],
    [('nenhum', ('PROAJD', 'PROSUB'))],
    [('nenhuma', ('PROADJ', 'PROSUB'))],
    [('nada', ('PROADJ', 'PROSUB'))],
    [('nunca', 'ADV')],
    [('jamais', 'ADV')],
]

AND = [('e', 'KC')]

OR = [('ou', 'KC')]

IF = [('se', 'KS')]


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
    # (('e', 'KC'))

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


class LogicOperatorsIncidence(base.Metric):
    """"""
    def __init__(self, name='Logic operators incidence',
                 column_name='logic_operators'):
        super(LogicOperatorsIncidence, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        occurrences = [count_occurrences_for_all(sent, LOGIC_OPERATORS,
                                                 ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class AndIncidence(base.Metric):
    """Docstring for AndIncidence. """
    def __init__(self, name='Incidence of ANDs.', column_name='and_incidence'):
        super(AndIncidence, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        occurrences = [count_occurrences(sent, AND, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class OrIncidence(base.Metric):
    """Docstring for OrIncidence. """
    def __init__(self, name='Incidence of ORs.', column_name='or_incidence'):
        super(OrIncidence, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        occurrences = [count_occurrences(sent, OR, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class IfIncidence(base.Metric):
    """Docstring for IfIncidence. """
    def __init__(self, name='Incidence of IFs.', column_name='if_incidence'):
        super(IfIncidence, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        occurrences = [count_occurrences(sent, IF, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class NegationIncidence(base.Metric):
    """Docstring for NegationIncidence. """
    def __init__(self, name='Incidence of negations',
                 column_name='negation_incidence'):
        super(NegationIncidence, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        occurrences = [count_occurrences_for_all(sent, NEGATIONS,
                                                 ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class LogicOperators(base.Category):
    """
    """
    def __init__(self, name='Logic operators', table_name='logic_operators'):
        super(LogicOperators, self).__init__(name, table_name)
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp, ignore_pos=False):
        metrics_values = base.ResultSet([(m, m.value_for_text(t))
                                         for m in self.metrics])
        return metrics_values


def test():
    print(count_occurrences([('O', 'ART'), ('gato', 'N'), ('correu', 'V'),
                             ('e', 'KC'), ('sumiu', 'V'), ('.', 'PU')],
                            LOGIC_OPERATORS[0]))
    print(count_occurrences([('Ele', 'PROPESS'), ('entra', 'V'), (',', 'PU'),
                             ('contanto', 'KS'), ('que', 'KS'),
                             ('saia', 'V'), ('.', 'PU')],
                            LOGIC_OPERATORS[12]))
    print(count_occurrences_for_all([('Ele', 'PROPESS'), ('entra', 'V'),
                                     (',', 'PU'), ('contanto', 'KS'),
                                     ('que', 'KS'), ('saia', 'V'), ('e', 'KC'),
                                     ('feche', 'V'), ('a', 'ART'),
                                     ('porta', 'N'), ('.', 'PU')],
                                    LOGIC_OPERATORS))
    lo = LogicOperators()
    t = base.Text(base_path + '/corpora/folha/folha0.txt')
    results = lo.values_for_text(t)
    print(results)
