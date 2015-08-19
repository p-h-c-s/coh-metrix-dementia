# -*- coding: utf-8 -*-
# Coh-Metrix-Dementia - Automatic text analysis and classification for dementia.
# Copyright (C) 2014  Andre Luiz Verucci da Cunha
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

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
    Incidência de Conectivos:

        Incidência de todos os conectivos que aparecem em um texto. Para esta
        métrica (e as demais que contam conectivos) compilamos listas de
        conectivos classificados em duas dimensões. A primeira dimensão divide
        os conectivos em positivos e negativos (conectivos positivos estendem
        eventos, enquanto que conectivos negativos param eventos). A segunda
        dimensão divide os conectivos de acordo com o tipo de coesão: aditivos,
        temporais, lógicos e causais.

        Exemplo:

            "O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."

            Como há 6 conectivos e 95 palavras, a incidência de conectivos é
            63,157 (número de conectivos/(número de palavras/1000)).
    """
    name = 'Connectives incidence'
    column_name = 'conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_all_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class AddPosConnectivesIncidence(base.Metric):
    """
    Incidência de conectivos classificados como aditivos positivos.

        Incidência de todos os conectivos positivos que aparecem em um texto.

        Exemplo:

            "O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."

            Como há 5 conectivos positivos e 95 palavras, a incidência de
            conectivos positivos é 52,631 (número de conectivos positivos/
            (número de palavras/1000)).
    """
    name = 'Incidence of additive positive connectives'
    column_name = 'add_pos_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_add_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class AddNegConnectivesIncidence(base.Metric):
    """
    Incidência de conectivos classificados como aditivos negativos.

        Incidência de todos os conectivos negativos que aparecem em um texto.

        Exemplo:

            "Entretanto, foram encontrados vários problemas clássicos."

            Como há 1 conectivos negativos (entretanto) e 6 palavras, a
            incidência de conectivos negativos é 166,666 (número de conectivos
            positivos/(número de palavras/1000)).
    """
    name = 'Incidence of additive negative connectives'
    column_name = 'add_neg_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_add_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class TmpPosConnectivesIncidence(base.Metric):
    """
    Incidência de conectivos classificados como temporais positivos.

        Incidência de todos os conectivos temporais positivos que aparecem em
        um texto.

        Exemplo:

            "Enquanto isso, mais de 100 pessoas tentam resolver o problema, o
            que finalmente resultou em bons resultados."

            Como há 2 conectivos temporais positivos (enquanto e finalmente) e
            6 palavras, a incidência de conectivos temporais positivos é
            117,647 (número de conectivos temporais positivos/(número
            de palavras/1000)).
    """
    name = 'Incidence of temporal positive connectives'
    column_name = 'tmp_pos_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_tmp_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class TmpNegConnectivesIncidence(base.Metric):
    """
    Incidência de conectivos classificados como temporais negativos.

        Incidência de todos os conectivos temporais negativos que aparecem em
        um texto.

        Exemplo:

            "O menino colou na prova até que a professora descobriu sua
            artimanha."

            Como há 1 conectivos temporais negativo (até) e
            12 palavras, a incidência de conectivos temporais negativos é
            83,333 (número de conectivos temporais negativos/(número
            de palavras/1000)).
    """
    name = 'Incidence of temporal negative connectives'
    column_name = 'tmp_neg_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_tmp_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class CauPosConnectivesIncidence(base.Metric):
    """
    Incidência de conectivos classificados como causais positivos

        Incidência de todos os conectivos causais positivos que aparecem em
        um texto.

        Exemplo:

            "O menino queria ir bem na prova. Para isso, ele resolveu colar."

            Como há 1 conectivos causal positivo (Para isso) e
            12 palavras, a incidência de conectivos causais positivos é
            83,333 (número de conectivos causais positivos/(número
            de palavras/1000)).
    """
    name = 'Incidence of causal positive connectives'
    column_name = 'cau_pos_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_cau_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class CauNegConnectivesIncidence(base.Metric):
    """
    Incidência de conectivos classificados como causais negativos

        Incidência de todos os conectivos causais negativos que aparecem em
        um texto.

        Exemplo:

            "Embora tenha colado na prova, o menino não obteve uma boa nota."

            Como há 1 conectivos causal negativo (Para isso) e
            12 palavras, a incidência de conectivos causais negativos é
            83,333 (número de conectivos causais negativos/(número
            de palavras/1000)).
    """
    name = 'Incidence of causal negative connectives'
    column_name = 'cau_neg_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_cau_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class LogPosConnectivesIncidence(base.Metric):
    """
    Conectivos Lógicos Positivos

        Incidência de todos os conectivos lógicos positivos que aparecem em
        um texto.

        Exemplo:

            "Desde que o menino começou a colar nas provas, ele não estuda
            mais."

            Como há 1 conectivos lógico positivo (Desde que) e
            13 palavras, a incidência de conectivos lógicos positivos é
            76,923 (número de conectivos lógicos positivos/(número
            de palavras/1000)).
    """
    name = 'Incidence of logical positive connectives'
    column_name = 'log_pos_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_log_pos_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class LogNegConnectivesIncidence(base.Metric):
    """
    Conectivos Lógicos Negativos

        Incidência de todos os conectivos lógicos negativos que aparecem em
        um texto.

        Exemplo:

            "O menino colou na prova, embora soubesse que poderia ser pego."

            Como há 1 conectivos lógico negativo (Desde que) e
            11 palavras, a incidência de conectivos lógicos negativos é
            90,909 (número de conectivos lógicos negativos/(número
            de palavras/1000)).
    """
    name = 'Incidence of logical negative connectives'
    column_name = 'log_neg_conn_incidence'

    def value_for_text(self, t, rp=default_rp):
        connectives = get_log_neg_conn(rp)
        occurrences = [count_occurrences_for_all(sent, connectives,
                                                 ignore_pos=True)
                       for sent in rp.tagged_sentences(t)]

        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class Connectives(base.Category):
    """
    """
    name = 'Connectives'
    table_name = 'connectives'

    def __init__(self):
        super(Connectives, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
