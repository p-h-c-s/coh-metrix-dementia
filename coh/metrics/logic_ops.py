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
from coh.utils import base_path, count_occurrences, count_occurrences_for_all


class LogicOperatorsIncidence(base.Metric):
    """
        ## Incidência de Operadores Lógicos:

        Incidência de operadores lógicos em um texto. Consideramos como
        operadores lógicos: e, ou, se, negações e um número de condições.

        ### Exemplo:

        *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
            Já não temos recursos suficientes para a manutenção das escolas,
            por exemplo, e também precisamos valorizar o magistério - justifica
            a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*  

        Como há 4 operadores lógicos e 38 palavras a incidência de
            operadores lógicos é 105,26 (número de operadores lógicos/(número
            de palavras/1000)).
    """
    name = 'Logic operators incidence'
    column_name = 'logic_operators'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        logic_operators = rp.pos_tagger().tagset.LOGIC_OPERATORS
        occurrences = [count_occurrences_for_all(sent, logic_operators,
                                                 ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class AndIncidence(base.Metric):
    """
        ## Incidência do operador lógico E:

        Incidência do operador lógico E em um texto.

        ### Exemplo:

        *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
            Já não temos recursos suficientes para a manutenção das escolas,
            por exemplo, e também precisamos valorizar o magistério - justifica
            a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*  

        Como há 1 operadores lógicos E e 38 palavras a incidência do
            operadores lógico E é 26,315 (frequência do operador lógico E /
            (número de palavras/1000)).
    """
    name = 'Incidence of ANDs.'
    column_name = 'and_incidence'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        _and = rp.pos_tagger().tagset.AND
        occurrences = [count_occurrences(sent, _and, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class OrIncidence(base.Metric):
    """
        ## Incidência do operador lógico OU:

        Incidência do operador lógico OU em um texto.

        ### Exemplo:

        *"Os vermes – também chamados de helmintos – são parasitos, animais
            que, em geral, dependem da relação com outros seres para viver.
            Eles podem se hospedar no organismo de diversos animais, como bois,
            aves e peixes. Por isso, podemos também contraí-los comendo carnes
            cruas ou mal cozidas."*  

        Como há 1 operadores lógicos OU e 45 palavras a incidência do
            operadores lógico OU é 22,222 (frequência do operador lógico OU /
            (número de palavras/1000)).
    """
    name = 'Incidence of ORs.'
    column_name = 'or_incidence'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        _or = rp.pos_tagger().tagset.OR
        occurrences = [count_occurrences(sent, _or, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class IfIncidence(base.Metric):
    """
        ## Incidência do operador lógico SE:

        Incidência do operador lógico SE em um texto (desconsidera quando o SE
        é um pronome).

        ### Exemplo:

        *"O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."*  

        Como há 1 operadores lógicos SE e 95 palavras a incidência do
            operadores lógico SE é 10,526 (frequência do operador lógico SE /
            (número de palavras/1000)).
    """
    name = 'Incidence of IFs.'
    column_name = 'if_incidence'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        _if = rp.pos_tagger().tagset.IF
        occurrences = [count_occurrences(sent, _if, ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


class NegationIncidence(base.Metric):
    """
        ## Incidência de negação:

        Incidência de Negações. Consideramos como negações: não, nem, nenhum,
        nenhuma, nada, nunca e jamais.

        ### Exemplo:

        *"O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."*  

        No exemplo aparecem 3 negações. Como o mesmo possui 38 palavras a
            incidência de negações é 78,947 (número de negações/(número de
            palavras/1000)).
    """
    name = 'Incidence of negations'
    column_name = 'negation_incidence'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        negations = rp.pos_tagger().tagset.NEGATIONS
        occurrences = [count_occurrences_for_all(sent, negations,
                                                 ignore_pos)
                       for sent in rp.tagged_sentences(t)]
        return sum(occurrences) / (len(rp.all_words(t)) / 1000) \
            if len(rp.all_words(t)) else 0


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
