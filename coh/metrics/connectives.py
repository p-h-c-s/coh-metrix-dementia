# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from coh import base
from coh.resource_pool import rp as default_rp
from coh.utils import count_occurrences_for_all


_all_connectives = None


def convert(conn_list):
    """Converts a list of connectives into the format that is accepted by
    utils.count_occurrences and utils.count_occurrences_for_all.
    """
    def conn_to_list(conn):
        return [(word, 'NO_POS') for word in conn.connective.split(' ')]

    return [conn_to_list(conn) for conn in conn_list]


def load_connectives(rp):
    global _all_connectives
    if _all_connectives is None:
        _all_connectives = rp.db_helper().get_all_connectives()


def get_all_conn(rp):
    load_connectives(rp)
    return convert(_all_connectives)


def get_add_pos_conn(rp):
    load_connectives(rp)
    add_pos_conn = [conn for conn in _all_connectives if conn.additive_pos]

    return convert(add_pos_conn)


def get_add_neg_conn(rp):
    load_connectives(rp)
    add_neg_conn = [conn for conn in _all_connectives if conn.additive_neg]

    return convert(add_neg_conn)


def get_tmp_pos_conn(rp):
    load_connectives(rp)
    tmp_pos_conn = [conn for conn in _all_connectives if conn.temporal_pos]

    return convert(tmp_pos_conn)


def get_tmp_neg_conn(rp):
    load_connectives(rp)
    tmp_neg_conn = [conn for conn in _all_connectives if conn.temporal_neg]

    return convert(tmp_neg_conn)


def get_cau_pos_conn(rp):
    load_connectives(rp)
    cau_pos_conn = [conn for conn in _all_connectives if conn.causal_pos]

    return convert(cau_pos_conn)


def get_cau_neg_conn(rp):
    load_connectives(rp)
    cau_neg_conn = [conn for conn in _all_connectives if conn.causal_neg]

    return convert(cau_neg_conn)


def get_log_pos_conn(rp):
    load_connectives(rp)
    log_pos_conn = [conn for conn in _all_connectives if conn.logic_pos]

    return convert(log_pos_conn)


def get_log_neg_conn(rp):
    load_connectives(rp)
    log_neg_conn = [conn for conn in _all_connectives if conn.logic_neg]

    return convert(log_neg_conn)


class ConnectivesIncidence(base.Metric):
    """
    """
    name = 'Connectives incidence'
    column_name = 'conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_all_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t))


class AddPosConnectivesIncidence(base.Metric):
    """
    """
    name = 'Incidence of additive positive connectives'
    column_name = 'add_pos_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_add_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t))


class AddNegConnectivesIncidence(base.Metric):
    """
    """
    name = 'Incidence of additive negative connectives'
    column_name = 'add_neg_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_add_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t))


class TmpPosConnectivesIncidence(base.Metric):
    """
    """
    name = 'Incidence of temporal positive connectives'
    column_name = 'tmp_pos_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_tmp_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t))


class TmpNegConnectivesIncidence(base.Metric):
    """
    """
    name = 'Incidence of temporal negative connectives'
    column_name = 'tmp_neg_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_tmp_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t))


class CauPosConnectivesIncidence(base.Metric):
    """
    """
    name = 'Incidence of causal positive connectives'
    column_name = 'cau_pos_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_cau_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t))


class CauNegConnectivesIncidence(base.Metric):
    """
    """
    name = 'Incidence of causal negative connectives'
    column_name = 'cau_neg_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_cau_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t))


class LogPosConnectivesIncidence(base.Metric):
    """
    """
    name = 'Incidence of logical positive connectives'
    column_name = 'log_pos_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_log_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t))


class LogNegConnectivesIncidence(base.Metric):
    """
    """
    name = 'Incidence of logical negative connectives'
    column_name = 'log_neg_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_log_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / len(rp.all_words(t))


class Connectives(base.Category):
    """
    """
    name = 'Connectives'
    table_name = 'connectives'

    def __init__(self):
        super(Connectives, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
