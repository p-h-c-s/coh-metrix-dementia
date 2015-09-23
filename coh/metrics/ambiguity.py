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


def calculate_ambiguity(rp, t, delaf_tag, tep_tag, checker):
    """Calculates the ambiguity metric for a word category, which is the average
    number of meanings of the words belonging to this category in the text.

    :rp: the resource pool to be used.
    :t: the text to be analyzed.
    :delaf_tag: the corresponding PoS tag used in the DELAF tables.
    :tep_tag: the corresponding PoS tag used in the Tep tables.
    :checker: a function that returns True iff a token is of the desired
    category

    :returns: the ratio between the total number of meanings and the total
    number of words for a given category.

    """

    words = [word.lower() for (word, tag) in rp.tagged_words(t)
             if checker((word, tag))]

    word_stems = [rp.stemmer().get_lemma(word, delaf_tag) for word in words]
    word_stems = [word for word in word_stems if word is not None]

    meanings_count = [rp.db_helper().get_tep_words_count(stem, tep_tag)
                      for stem in word_stems]
    meanings_count = [m for m in meanings_count if m is not None]

    return sum(meanings_count) / len(words) if words else 0


class VerbAmbiguity(base.Metric):
    """
        ## Ambiguidade de Verbos:

        Para cada verbo do texto soma-se o número de sentidos apresentados no
        TEP (Maziero et. al., 2008) e divide o total pelo número de verbos.

        O desempenho da métrica é diretamente relacionado ao desempenho do
        dicionário do TEP.

        ### Exemplo:

        *"O menino colou na prova, embora soubesse que poderia ser pego."*

        O exemplo apresenta 4 verbos (__colou__, __soubesse__, __poderia__ e
        __ser__) com frequências 4, 7, 2 e 12 no TEP. O resultado da métrica
        é 6,25.
    """

    name = 'Ambiguity of verbs'
    column_name = 'verbs_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'V', 'Verbo',
                                   rp.pos_tagger().tagset.is_verb)


class NounAmbiguity(base.Metric):
    """
        ## Ambiguidade de Substantivos:

        Para cada substantivo do texto soma-se o número de sentidos
        apresentados no TEP (Maziero et. al., 2008) e divide o total pelo
        número de substantivos.

        O desempenho da métrica é diretamente relacionado ao desempenho do
        dicionário do TEP.

        ### Exemplo:

        *"O menino colou na prova, embora soubesse que poderia ser pego."*

        O exemplo apresenta 2 substantivos (__menino__ e __prova__) com
            frequências 1 e 9 no TEP. O resultado da métrica é 5,0.
    """

    name = 'Ambiguity of nouns'
    column_name = 'nouns_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'N', 'Substantivo',
                                   rp.pos_tagger().tagset.is_noun)


class AdjectiveAmbiguity(base.Metric):
    """
        ## Ambiguidade de Adjetivos:

        Para cada adjetivo do texto soma-se o número de sentidos apresentados
        no TEP (Maziero et. al., 2008) e divide o total pelo número de
        adjetivos.

        O desempenho da métrica é diretamente relacionado ao desempenho do
        dicionário do TEP.

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

        Dos adjetivos rotulados no texto exemplo (__polêmico__, __municipal__,
            __estadual__, __federal__, __solar__, __anual__), consta apenas
            __anual__ no TEP. Assim, o valor da métrica é 0,166.
    """

    name = 'Ambiguity of adjectives'
    column_name = 'adjectives_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'A', 'Adjetivo',
                                   rp.pos_tagger().tagset.is_adjective)


class AdverbAmbiguity(base.Metric):
    """
        ## Ambiguidade de Advérbios

        Para cada advérbio do texto soma-se o número de sentidos apresentados
        no TEP (Maziero et. al., 2008) e divide o total pelo número de
        advérbios.

        O desempenho da métrica é diretamente relacionado ao desempenho do
        dicionário do TEP.

        ### Exemplo:

        *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
            Já não temos recursos suficientes para a manutenção das escolas,
            por exemplo, e também precisamos valorizar o magistério - justifica
            a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*

        Os advérbios rotulados no texto exemplo são: __não__, __mais__, __já__,
            __não__ com sentidos: 1, 5, 4, 1. Assim, o valor da métrica é 2,2.
    """

    name = 'Ambiguity of adverbs'
    column_name = 'adverbs_ambiguity'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'ADV', 'Advérbio',
                                   rp.pos_tagger().tagset.is_adverb)


class Ambiguity(base.Category):
    name = 'Ambiguity'
    table_name = 'ambiguity'

    def __init__(self):
        super(Ambiguity, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
