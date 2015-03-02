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
import re
from coh import base
from coh.resource_pool import rp as default_rp


class AnaphoricReferencesBase(base.Metric):

    """Docstring for AnaphoricReferencesBase. """

    name = 'Adjacent anaphoric references'
    column_name = 'adjacent_refs'

    referents = {r'^elas$': 'fp',
                 r'^nelas$': 'fp',
                 r'^delas$': 'fp',
                 r'^.*-nas$': 'fp',
                 r'^.*-las$': 'fp',
                 r'^.*-as$': 'fp',
                 r'^eles$': 'mp',
                 r'^neles$': 'mp',
                 r'^deles$': 'mp',
                 r'^.*-nos$': 'mp',
                 r'^.*-los$': 'mp',
                 r'^.*-os$': 'mp',
                 r'^ela$': 'fs',
                 r'^nela$': 'fs',
                 r'^dela$': 'fs',
                 r'^.*-na$': 'fs',
                 r'^.*-la$': 'fs',
                 r'^.*-a$': 'fs',
                 r'^ele$': 'ms',
                 r'^nele$': 'ms',
                 r'^dele$': 'ms',
                 r'^.*-no$': 'ms',
                 r'^.*-lo$': 'ms',
                 r'^.*-o$': 'ms',
                 r'^lhes$': 'ap',
                 r'^lhe$': 'as',
                 }

    def __init__(self, nsentences=1):
        """Form an AnaphoricReferencesBase object.

        :nsentences: the number of sentences to look back for anaphoric
            references.
        """
        self.nsentences = nsentences

        self.compiled_referents = {}
        for regex, category in self.referents.items():
            self.compiled_referents[regex] = re.compile(regex)

    def find_candidates(self, sentences, indices, category, rp):
        """Find nouns of a certain gender/number in a list of sentences.

        :sentences: the tagged sentences.
        :indices: the indices of the sentences to be searched.
        :category: the category of nouns to look for (ms, mp, fs, fp, as, ap).
        :rp: the resource pool to use.
        :returns: a list of nouns matching the category.
        """
        db = rp.db_helper()

        candidates = []
        for i in indices:
            if (i, category) not in self.computed_categories:
                sentence = sentences[i]
                curr_candidates = []

                for token in sentence:
                    if rp.pos_tagger().tagset.is_noun(token):
                        attrs = db.get_delaf_noun(token[0].lower())
                        if not attrs:
                            continue
                        if category == 'ap':
                            if attrs.morf in ('mp', 'fp'):
                                curr_candidates.append(token[0])
                        elif category == 'as':
                            if attrs.morf in ('ms', 'fs'):
                                curr_candidates.append(token[0])
                        else:
                            if attrs.morf == category:
                                curr_candidates.append(token[0])

                self.computed_categories[(i, category)] = curr_candidates

            candidates.extend(self.computed_categories[(i, category)])

        return candidates

    def value_for_text(self, t, rp=default_rp):
        tokens = rp.tagged_sentences(t)

        if len(tokens) <= 1:
            return 0

        ncandidates = 0
        self.computed_categories = {}
        for isent in range(1, len(tokens)):
            iprev_sents = range(max(isent - self.nsentences, 0), isent)

            for token in tokens[isent]:
                for ref, category in self.referents.items():
                    if self.compiled_referents[ref].match(token[0].lower()):
                        candidates = self.find_candidates(tokens, iprev_sents,
                                                          category, rp)
                        ncandidates += len(candidates)

        return ncandidates / len(tokens)


class AdjacentAnaphoricReferences(AnaphoricReferencesBase):
    def __init__(self):
        super(AdjacentAnaphoricReferences, self).__init__(nsentences=1)


class AnaphoricReferences(AnaphoricReferencesBase):
    def __init__(self):
        super(AnaphoricReferences, self).__init__(nsentences=5)


class Anaphores(base.Category):
    """
    """
    name = 'Anaphores'
    table_name = 'anaphores'

    def __init__(self):
        super(Anaphores, self).__init__()
        self.metrics = [AdjacentAnaphoricReferences(),
                        AnaphoricReferences(), ]
        self.metrics.sort(key=lambda m: m.name)
