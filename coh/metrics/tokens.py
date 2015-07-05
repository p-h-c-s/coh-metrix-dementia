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
from coh.utils import find_subtrees
from collections import Counter
from math import log


class PersonalPronounsIncidence(base.Metric):
    """
    """
    name = 'Personal pronouns incidence'
    column_name = 'personal_pronouns'

    personal_pronouns = ['eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles',
                         'elas', 'você', 'vocês']

    def __init__(self):
        super(PersonalPronounsIncidence, self).__init__()

    def value_for_text(self, t, rp=default_rp):
        words = [word.lower() for word in rp.all_words(t)]
        n_personal_pronouns = sum([word in self.personal_pronouns
                                   for word in words])
        return n_personal_pronouns / (len(words) / 1000)


class PronounsPerNounPhrase(base.Metric):
    """
    """
    name = 'Mean pronouns per noun phrase'
    column_name = 'pronouns_per_np'

    def value_for_text(self, t, rp=default_rp):
        parse_trees = rp.parse_trees(t)

        sent_indices = []
        for i, tree in enumerate(parse_trees):
            nps = 0
            prons = 0

            for np in find_subtrees(tree, 'NP'):
                prons += len([tt for tt in np
                              if tt.label() in ('PRS')])
                nps += 1

            sent_indices.append(prons / nps)

        return sum(sent_indices) / len(sent_indices)


class TypeTokenRatio(base.Metric):
    """
    """
    name = 'Type to token ratio'
    column_name = 'ttr'

    def __init__(self):
        super(TypeTokenRatio, self).__init__()

    def value_for_text(self, t, rp=default_rp):
        tokens = rp.all_words(t)
        types = rp.token_types(t)

        ttr = len(types) / len(tokens)

        return ttr


class BrunetIndex(base.Metric):

    """Docstring for BrunetIndex. """

    name = 'Brunet Index'
    column_name = 'brunet'

    def value_for_text(self, t, rp=default_rp):
        tokens = rp.all_words(t)
        types = rp.token_types(t)

        W = len(tokens) ** len(types) ** -0.165

        return W


class HoroneStatistic(base.Metric):

    """Docstring for HoroneIndex. """

    name = 'Honore Statistic'
    column_name = 'honore'

    def value_for_text(self, t, rp=default_rp):
        tokens = [word.lower() for word in rp.all_words(t)]
        types = rp.token_types(t)

        counter = Counter(tokens)
        one_time_tokens = [word for word, count in counter.items()
                           if count == 1]

        R = 100 * log(len(tokens), 10) / (1 - len(one_time_tokens) / len(types))

        return R


class MeanClauseUtterance(base.Metric):
    """ Docstring for MeanClauseUtterance. """

    name = 'Mean Clauses per Utterance'
    column_name = 'mcu'

    def value_for_text(self, t, rp=default_rp):
        # We estimate the number of clauses by the number of S nodes in
        # the syntax tree that have a VP node.
        trees = rp.parse_trees(t)

        clauses = []
        for tree in trees:
            n_clauses = 0
            for subtree in tree.subtrees(lambda t: t.height() >= 3):
                if subtree.label() == 'S':
                    sub_vps = [t for t in subtree if t.label() == 'VP']
                    n_clauses += len(sub_vps)
            clauses.append(n_clauses)

        return sum(clauses) / len(clauses)


class Tokens(base.Category):
    name = 'Pronouns, Types and Tokens'
    table_name = 'tokens'

    def __init__(self):
        super(Tokens, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(Tokens, self).values_for_text(t, rp)
