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
import idd3
from coh import base
from coh.resource_pool import rp as default_rp


class MeanPauseDuration(base.Metric):
    """ """

    name = 'Mean pause duration'
    column_name = 'mean_pause'

    pause_pattern = re.compile(r'\(\(pausa\s+(\d+)\s*\w*\)\)')

    def value_for_text(self, t, rp=default_rp):
        content = rp.raw_content(t)
        words = rp.raw_words(t)

        pauses = [int(duration)
                  for duration in self.pause_pattern.findall(content)]

        return sum(pauses) / len(words) if words else 0


class MeanShortPauses(base.Metric):
    """"""

    name = "Mean # of short pauses"
    column_name = 'mean_short_pauses'

    short_pause_pattern = re.compile(r'\.\.\.')

    def value_for_text(self, t, rp=default_rp):
        content = rp.raw_content(t)
        words = rp.raw_words(t)

        pauses = self.short_pause_pattern.findall(content)

        return len(pauses) / len(words) if words else 0


class MeanVowelStretchings(base.Metric):
    """ """
    
    name = 'Mean # of vowel stretchings'
    column_name = 'mean_vowel'

    stretching_pattern = re.compile(r'::+')

    def value_for_text(self, t, rp=default_rp):
        content = rp.raw_content(t)
        words = rp.raw_words(t)

        stretchings = self.stretching_pattern.findall(content)

        return len(stretchings) / len(words) if words else 0


class MeanEmpty(base.Metric):
    """ """

    name = "Mean # of empty words"
    column_name = 'mean_empty'

    def value_for_text(self, t, rp=default_rp):
        words = rp.raw_words(t)

        empty_length = []
        for e in t.meta['empty']:
            text = re.sub(r"\.\.\.", ' ', e.text, re.U)
            text = re.sub(r'::', ' ', text, re.U)

            empty_words = [w for w in text.split(' ') if w]
            empty_length.append(len(empty_words))

        return sum(empty_length) / len(words) if words else 0


class MeanDisf(base.Metric):
    """ """

    name = "Mean # of disfluent words"
    column_name = 'mean_disf'

    def value_for_text(self, t, rp=default_rp):
        words = rp.raw_words(t)

        disf_length = []
        for e in t.meta['disf']:
            text = re.sub(r"\.\.\.", ' ', e.text, re.U)
            text = re.sub(r'::', ' ', text, re.U)

            disf_words = [w for w in text.split(' ') if w]
            print(disf_words)
            disf_length.append(len(disf_words))

        return sum(disf_length) / len(words) if words else 0


class Repetition(base.Metric):
    """ """

    name = "Ratio of repeated words"
    column_name = 'repetition'

    def value_for_text(self, t, rp=default_rp):
        raw_words = rp.raw_words(t)

        n_repeated_words = 0
        i = 0
        while i < len(raw_words):
            run_length = 0
            for j in range(i + 1, len(raw_words)):
                if raw_words[j] == raw_words[i]:
                    run_length += 1
                else:
                    break
            n_repeated_words += run_length

            i += run_length + 1

        return n_repeated_words / len(raw_words) if raw_words else 0


class TotalIdeaDensity(base.Metric):
    name = 'Total Idea Density'
    column_name = 'total_id'

    def value_for_text(self, t, rp=default_rp):
        engine = rp.idd3_engine()
        graphs = rp.dep_trees(t)
        raw_words = rp.raw_words(t)
        
        total_nprops = 0
        for index in range(len(graphs)):
            relations = []
            for relation in graphs[index].nodes.values():
                relations.append(idd3.Relation(**relation))

            # print('Propositions:')
            try:
                engine.analyze(relations)
                # for i, prop in enumerate(engine.props):
                #     print(str(i + 1) + ' ' + str(prop))

                n_props = len(engine.props)
            except Exception as e:
                n_props = 0

            # print(len(sents[index]), n_props / len(sents[index]) )
            total_nprops += n_props

        return total_nprops / len(raw_words) if raw_words else 0

    
class Disfluencies(base.Category):
    name = 'Disfluencies'
    table_name = 'disfluencies'

    def __init__(self):
        super(Disfluencies, self).__init__()
        self._set_metrics_from_module(__name__)
