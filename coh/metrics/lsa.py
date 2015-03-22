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
from coh.utils import adjacent_pairs, all_pairs
import numpy as np
from coh.tools import senter, word_tokenize
from itertools import chain


class LsaBase(base.Metric):
    """A base class for LSA-derived metrics."""

    def get_pairs(self, t, rp):
        """Return an iterator that yields pair of lists of strings."""

        raise NotImplementedError('Subclasses should override this method')

    def get_value(self, similarities):
        """Given a list of similarities between pairs, return the value of
        the metric.
        """

        raise NotImplementedError('Subclasses should override this method')

    def value_for_text(self, t, rp=default_rp):
        space = rp.lsa_space()
        similarities = []
        for s1, s2 in self.get_pairs(t, rp):
            similarities.append(space.compute_similarity(s1, s2))

        if not similarities:
            return 0
        return self.get_value(similarities)


class LsaSentenceAdjacentMean(LsaBase):
    """."""
    name = 'LSA sentence adjacent mean'
    column_name = 'LSASS1'

    def get_pairs(self, t, rp):
        tokens = rp.tokens(t)
        tokens = [[token.lower() for token in sentence] for sentence in tokens]

        return adjacent_pairs(tokens)

    def get_value(self, similarities):
        return sum(similarities) / len(similarities)


class LsaSentenceAdjacentSD(LsaBase):
    """."""
    name = 'LSA sentence adjacent SD'
    column_name = 'LSASS1d'

    def get_pairs(self, t, rp):
        tokens = rp.tokens(t)
        tokens = [[token.lower() for token in sentence] for sentence in tokens]

        return adjacent_pairs(tokens)

    def get_value(self, similarities):
        return np.array(similarities).std()


class LsaSentenceAllMean(LsaBase):
    """."""
    name = 'LSA sentence all mean'
    column_name = 'LSASSp'

    def get_pairs(self, t, rp):
        tokens = rp.tokens(t)
        tokens = [[token.lower() for token in sentence] for sentence in tokens]

        return all_pairs(tokens)

    def get_value(self, similarities):
        return sum(similarities) / len(similarities)


class LsaSentenceAllSD(LsaBase):
    """."""
    name = 'LSA sentence all (within paragraph) SD'
    column_name = 'LSASSpd'

    def get_pairs(self, t, rp):
        for paragraph in rp.paragraphs(t):
            sentences = senter.tokenize(paragraph)
            tokens = [word_tokenize(sent) for sent in sentences]

            for s1, s2 in all_pairs(tokens):
                yield s1, s2

    def get_value(self, similarities):
        return np.array(similarities).std()


def all_tokens(paragraph):
    """Return all tokens inside a paragraph in a list."""

    sentences = senter.tokenize(paragraph)
    tokens = [word_tokenize(sent) for sent in sentences]

    return list(chain.from_iterable(tokens))


class LsaParagraphAdjacentMean(LsaBase):
    """."""
    name = 'LSA paragraph adjacent mean'
    column_name = 'LSAPP1'

    def get_pairs(self, t, rp):
        paragraphs = [all_tokens(par) for par in rp.paragraphs(t)]
        return adjacent_pairs(paragraphs)

    def get_value(self, similarities):
        return sum(similarities) / len(similarities)


class LsaParagraphAdjacentSD(LsaBase):
    """."""
    name = 'LSA paragraph adjacent SD'
    column_name = 'LSAPP1d'

    def get_pairs(self, t, rp):
        paragraphs = [all_tokens(par) for par in rp.paragraphs(t)]
        return adjacent_pairs(paragraphs)

    def get_value(self, similarities):
        return np.array(similarities).std()


class LsaGivennessBase(LsaBase):

    def get_pairs(self, t, rp):
        tokens = rp.tokens(t)
        tokens = [[token.lower() for token in sentence] for sentence in tokens]

        for i in range(1, len(tokens)):
            past_sentences = tokens[:i]
            past_tokens = list(chain.from_iterable(past_sentences))

            yield tokens[i], past_tokens


class LsaGivennessMean(LsaGivennessBase):
    """Docstring for LsaGivennessMean. """

    name = 'LSA sentence givenness mean'
    column_name = 'LSAGN'

    def get_value(self, similarities):
        return sum(similarities) / len(similarities)


class LsaGivennessSD(LsaGivennessBase):
    """Docstring for LsaGivennessMean. """

    name = 'LSA sentence givenness SD'
    column_name = 'LSAGNd'

    def get_value(self, similarities):
        return np.array(similarities).std()


class Lsa(base.Category):
    name = 'Latent Semantic Analysis'
    table_name = 'lsa'

    def __init__(self):
        super(Lsa, self).__init__()
        self.metrics = [LsaSentenceAdjacentMean(),
                        LsaSentenceAdjacentSD(),
                        LsaSentenceAllMean(),
                        LsaSentenceAllSD(),
                        LsaParagraphAdjacentMean(),
                        LsaParagraphAdjacentSD(),
                        LsaGivennessMean(),
                        LsaGivennessSD(),
                        ]
