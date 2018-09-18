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

# --- Base classes ---


class CoreferenceBase(base.Metric):
    """Docstring for CoreferenceBase. """

    def get_sentences(self, text, rp):
        """TODO: Docstring for get_sentences.

        :text: TODO
        :rp: TODO
        :returns: TODO

        """
        raise NotImplementedError('Subclasses must override this method.')

    @staticmethod
    def word_pairs(s1, s2):
        """TODO: Docstring for generate_word_pairs.

        :s1: TODO
        :s2: TODO
        :returns: TODO

        """
        for w1 in s1:
            for w2 in s2:
                yield w1.lower(), w2.lower()

    def sentence_pairs(self, text, rp):
        """TODO: Docstring for is_match.

        :src: TODO
        :dst: TODO
        :returns: TODO

        """
        raise NotImplementedError('Subclasses must override this method.')

    def value_for_text(self, t, rp=default_rp):
        if len(rp.sentences(t)) <= 1:
            return 0

        matches = 0
        pairs = 0
        for s1, s2 in self.sentence_pairs(t, rp):
            for w1, w2 in self.word_pairs(s1, s2):
                if w1 == w2:
                    matches += 1
            pairs += 1

        return matches / pairs if pairs else 0


class AdjacentOverlapBase(CoreferenceBase):
    """Docstring for AdjacentOverlapBase. """

    def sentence_pairs(self, text, rp):
        sentences = self.get_sentences(text, rp)

        for i in range(1, len(sentences)):
            yield sentences[i], sentences[i - 1]


class OverlapBase(CoreferenceBase):
    """Docstring for OverlapBase. """

    def sentence_pairs(self, text, rp):
        sentences = self.get_sentences(text, rp)

        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                yield sentences[i], sentences[j]


class ArgumentBase(CoreferenceBase):

    def get_sentences(self, text, rp):
        sentences = []
        tagset = rp.pos_tagger().tagset
        for sentence in rp.tagged_sentences(text):
            sentences.append([token[0] for token in sentence
                              if tagset.is_noun(token)
                              or tagset.is_pronoun(token)])

        return sentences


# --- Metric classes ---


class AdjacentArgumentOverlap(AdjacentOverlapBase, ArgumentBase):
    """
        ## Sobreposição de Argumentos Adjacentes:

        Proporção de sentenças adjacentes que compartilham um ou mais
        argumentos (substantivos, pronomes ou sintagmas nominais).

        O desempenho da métrica é diretamente relacionada ao do POS tagger do
        nlpnet.

        ### Exemplo:

        1. *Dentro do lago, existem peixes, como a traíra e o dourado,
             além da palometa, um tipo de piranha.*
        2. *Ela é uma espécie carnívora que se alimenta de peixes.*
        3. *No verão, elas ficam mais próximas das margens da barragem,
             atraídas pela movimentação das pessoas e por restos de comida que
             alguns turistas deixam na água quando lavam os pratos.*

        Para este exemplo temos que as sentenças (1) e (2) compartilham
             um substantivo (peixes) e, portanto, este par incrementa 1 no
             valor de correferência. Como também há dois pares de sentenças
             adjacentes ((1) com (2) e (2) com (3)), o valor final da métrica
             é 1/2 = 0,5.
    """

    name = 'Adjacent argument overlap'
    column_name = 'adj_arg_ovl'


class ArgumentOverlap(OverlapBase, ArgumentBase):
    """
        ## Sobreposição de Argumentos:

        Proporção de todos os pares de sentenças que compartilham um ou mais
        argumentos (substantivos, pronomes ou sintagmas nominais).

        O desempenho da métrica é diretamente relacionada ao do POS tagger do
        nlpnet.

        ### Exemplo:

        1. *Dentro do lago, existem peixes, como a traíra e o dourado,
             além da palometa, um tipo de piranha.*
        2. *Ela é uma espécie carnívora que se alimenta de peixes.*
        3. *No verão, elas ficam mais próximas das margens da barragem,
             atraídas pela movimentação das pessoas e por restos de comida que
             alguns turistas deixam na água quando lavam os pratos.*

        Para este exemplo temos os pares de sentenças (1) com (2), (1)
             com (3) e (2) com (3). Como somente o par (1) com (2) compartilham
             um substantivo (peixes) o valor final da métrica é 1/3 = 0,333.
    """

    name = 'Argument overlap'
    column_name = 'arg_ovl'


class AdjacentStemOverlap(AdjacentOverlapBase):
    """
        ## Sobreposição de Radicais de palavras Adjacentes:

        Proporção de sentenças adjacentes que compartilham radicais.

        ### Exemplo:

        1. *Dentro do lago, existem peixes, como a traíra e o dourado,
             além da palometa, um tipo de piranha.*
        2. *Ela é uma espécie carnívora que se alimenta de peixes.*
        3. *No verão, elas ficam mais próximas das margens da barragem,
             atraídas pela movimentação das pessoas e por restos de comida que
             alguns turistas deixam na água quando lavam os pratos.*

        Neste exemplo, para sentenças adjacentes, temos que (1) e (2)
             compartilham o radical "peix". Como há dois pares de sentenças
             adjacentes e somente um compartilha um radical, então o
             resultado da métrica é 1/2 = 0,5.
    """

    name = 'Adjacent stem overlap'
    column_name = 'adj_stem_ovl'

    def get_sentences(self, text, rp):
        return rp.stemmed_content_words(text)


class StemOverlap(OverlapBase):
    """
        ## Sobreposição de Radicais de palavras:

        Proporção de todos os pares de sentenças que compartilham radicais.

        ### Exemplo:

        1. *Dentro do lago, existem peixes, como a traíra e o dourado,
             além da palometa, um tipo de piranha.*
        2. *Ela é uma espécie carnívora que se alimenta de peixes.*
        3. *No verão, as piranhas ficam mais próximas das margens da
             barragem, atraídas pela movimentação das pessoas e por restos de
             comida que alguns turistas deixam na água quando lavam os
             pratos.*

        Neste exemplo, além de (1) e (2), (1) e (3) também compartilham
             um radical (piranh). Então, como são três os possíveis pares, o
             valor final da métrica é 2/3 = 0,667.
    """

    name = 'Stem overlap'
    column_name = 'stem_ovl'

    def get_sentences(self, text, rp):
        return rp.stemmed_content_words(text)


class AdjacentContentWordOverlap(AdjacentOverlapBase):
    """
        ## Sobreposição de Palavras de conteúdo em sentenças adjacentes:

        Proporção de sentenças adjacentes que compartilham palavras de
        conteúdo (substantivos, verbos, adjetivos e advérbios).

        O desempenho da métrica é diretamente relacionada ao do POS tagger do
        nlpnet.

        ### Exemplo:

        1. *Dentro do lago, existem peixes, como a traíra e o dourado,
             além da palometa, um tipo de piranha.*
        2. *Ela é uma espécie carnívora que se alimenta de peixes.*
        3. *No verão, as piranhas ficam mais próximas das margens da
             barragem, atraídas pela movimentação das pessoas e por restos de
             comida que alguns turistas deixam na água quando lavam os
             pratos.*

        Neste exemplo, além de (1) e (2), (1) e (3) também compartilham
             um radical (piranh). Então, como são três os possíveis pares, o
             valor final da métrica é 2/3 = 0,667.
    """

    name = 'Adjacent content word overlap'
    column_name = 'adj_cw_ovl'

    def get_sentences(self, text, rp):
        return rp.content_words(text)


class Coreference(base.Category):
    """"""

    name = 'Coreference'
    table_name = 'coreference'

    def __init__(self):
        super(Coreference, self).__init__()
        self.metrics = [AdjacentArgumentOverlap(),
                        ArgumentOverlap(),
                        AdjacentStemOverlap(),
                        StemOverlap(),
                        AdjacentContentWordOverlap(),
                        ]
