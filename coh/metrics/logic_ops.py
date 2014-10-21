# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from coh import base
from coh.resource_pool import rp as default_rp
from coh.utils import base_path, count_occurrences, count_occurrences_for_all


class LogicOperatorsIncidence(base.Metric):
    """
    """
    name = 'Logic operators incidence'
    column_name = 'logic_operators'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        logic_operators = rp.pos_tagger().tagset.LOGIC_OPERATORS
        occurrences = [count_occurrences_for_all(sent, logic_operators,
                                                 ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class AndIncidence(base.Metric):
    """
    """
    name = 'Incidence of ANDs.'
    column_name = 'and_incidence'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        _and = rp.pos_tagger().tagset.AND
        occurrences = [count_occurrences(sent, _and, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class OrIncidence(base.Metric):
    """
    """
    name = 'Incidence of ORs.'
    column_name = 'or_incidence'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        _or = rp.pos_tagger().tagset.OR
        occurrences = [count_occurrences(sent, _or, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class IfIncidence(base.Metric):
    """
    """
    name = 'Incidence of IFs.'
    column_name = 'if_incidence'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        _if = rp.pos_tagger().tagset.IF
        occurrences = [count_occurrences(sent, _if, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class NegationIncidence(base.Metric):
    """
    """
    name = 'Incidence of negations'
    column_name = 'negation_incidence'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        negations = rp.pos_tagger().tagset.NEGATIONS
        occurrences = [count_occurrences_for_all(sent, negations,
                                                 ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / len(rp.all_words(t))


class LogicOperators(base.Category):
    """
    """
    name = 'Logic operators'
    table_name = 'logic_operators'

    def __init__(self):
        super(LogicOperators, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp, ignore_pos=False):
        metrics_values = base.ResultSet([(m, m.value_for_text(t))
                                         for m in self.metrics])
        return metrics_values


def test():
    logic_operators = default_rp.pos_tagger().tagset.LOGIC_OPERATORS
    print(count_occurrences([('O', 'ART'), ('gato', 'N'), ('correu', 'V'),
                             ('e', 'KC'), ('sumiu', 'V'), ('.', 'PU')],
                            logic_operators[0]))
    print(count_occurrences([('Ele', 'PROPESS'), ('entra', 'V'), (',', 'PU'),
                             ('contanto', 'KS'), ('que', 'KS'),
                             ('saia', 'V'), ('.', 'PU')],
                            logic_operators[12]))
    print(count_occurrences_for_all([('Ele', 'PROPESS'), ('entra', 'V'),
                                     (',', 'PU'), ('contanto', 'KS'),
                                     ('que', 'KS'), ('saia', 'V'), ('e', 'KC'),
                                     ('feche', 'V'), ('a', 'ART'),
                                     ('porta', 'N'), ('.', 'PU')],
                                    logic_operators))
    lo = LogicOperators()
    t = base.Text(base_path + '/corpora/folha/folha0.txt')
    results = lo.values_for_text(t)
    print(results)
