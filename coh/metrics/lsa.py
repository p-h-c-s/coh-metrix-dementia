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
from numpy import dot
from scipy.linalg import pinv
from gensim.matutils import cossim, sparse2full, full2sparse
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
    column_name = 'adj_mean'

    def get_pairs(self, t, rp):
        tokens = rp.tokens(t)
        tokens = [[token.lower() for token in sentence] for sentence in tokens]

        return adjacent_pairs(tokens)

    def get_value(self, similarities):
        return sum(similarities) / len(similarities) if similarities else 0


class LsaSentenceAdjacentStd(LsaBase):
    """."""
    name = 'LSA sentence adjacent std'
    column_name = 'adj_std'

    def get_pairs(self, t, rp):
        tokens = rp.tokens(t)
        tokens = [[token.lower() for token in sentence] for sentence in tokens]

        return adjacent_pairs(tokens)

    def get_value(self, similarities):
        return np.array(similarities).std()


class LsaSentenceAllMean(LsaBase):
    """."""
    name = 'LSA sentence all mean'
    column_name = 'all_mean'

    def get_pairs(self, t, rp):
        tokens = rp.tokens(t)
        tokens = [[token.lower() for token in sentence] for sentence in tokens]

        return all_pairs(tokens)

    def get_value(self, similarities):
        return sum(similarities) / len(similarities) if similarities else 0


class LsaSentenceAllStd(LsaBase):
    """."""
    name = 'LSA sentence all (within paragraph) std'
    column_name = 'all_std'

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
    column_name = 'paragraph_mean'

    def get_pairs(self, t, rp):
        paragraphs = [all_tokens(par) for par in rp.paragraphs(t)]
        return adjacent_pairs(paragraphs)

    def get_value(self, similarities):
        return sum(similarities) / len(similarities) if similarities else 0


class LsaParagraphAdjacentStd(LsaBase):
    """."""
    name = 'LSA paragraph adjacent std'
    column_name = 'paragraph_std'

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
    column_name = 'givenness_mean'

    def get_value(self, similarities):
        return sum(similarities) / len(similarities) if similarities else 0


class LsaGivennessStd(LsaGivennessBase):
    """Docstring for LsaGivennessStd. """

    name = 'LSA sentence givenness std'
    column_name = 'givenness_std'

    def get_value(self, similarities):
        return np.array(similarities).std()


class LsaSpanBase(base.Metric):
    """A base class for LSA span metrics."""

    def get_value(self, similarities):
        """Given a list of similarities between sentences and the span of the
        previous text, return the value of the metric.
        """

        raise NotImplementedError('Subclasses should override this method')

    def value_for_text(self, t, rp=default_rp):
        space = rp.lsa_space()
        num_topics = space.num_topics

        tokens = rp.tokens(t)
        tokens = [[token.lower() for token in sentence] for sentence in tokens]

        if len(tokens) < 2:
            return 0

        spans = np.zeros(len(tokens) - 1)
        for i in range(1, len(tokens)):
            past_sentences = tokens[:i]
            span_dim = len(past_sentences)

            if span_dim > num_topics - 1:
                # It's not clear, from the papers I read, what should be done
                # in this case. I did what seemed to not imply in loosing
                # information.
                beginning = past_sentences[0:span_dim - num_topics]
                past_sentences[0] = list(chain.from_iterable(beginning))

            past_vectors = [sparse2full(space.get_vector(sent), num_topics)
                            for sent in past_sentences]

            curr_vector = sparse2full(space.get_vector(tokens[i]), num_topics)
            curr_array = np.array(curr_vector).reshape(num_topics, 1)

            A = np.array(past_vectors).transpose()

            projection_matrix = dot(dot(A,
                                        pinv(dot(A.transpose(),
                                                 A))),
                                    A.transpose())

            projection = dot(projection_matrix, curr_array).ravel()

            spans[i - 1] = cossim(full2sparse(curr_vector),
                                  full2sparse(projection))

        return self.get_value(spans)


class LsaSpanMean(LsaSpanBase):
    """Docstring for LsaSpanMean. """

    name = 'LSA sentence span mean'
    column_name = 'span_mean'

    def get_value(self, spans):
        return spans.mean()


class LsaSpanStd(LsaSpanBase):
    """Docstring for LsaSpanStd. """

    name = 'LSA sentence span std'
    column_name = 'span_std'

    def get_value(self, spans):
        return spans.std()


class Lsa(base.Category):
    name = 'Latent Semantic Analysis'
    table_name = 'lsa'

    def __init__(self):
        super(Lsa, self).__init__()
        self.metrics = [LsaSentenceAdjacentMean(),
                        LsaSentenceAdjacentStd(),
                        LsaSentenceAllMean(),
                        LsaSentenceAllStd(),
                        LsaParagraphAdjacentMean(),
                        LsaParagraphAdjacentStd(),
                        LsaGivennessMean(),
                        LsaGivennessStd(),
                        LsaSpanMean(),
                        LsaSpanStd(),
                        ]
