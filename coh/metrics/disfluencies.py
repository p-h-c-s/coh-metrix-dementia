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


class Disfluencies(base.Category):
    name = 'Disfluencies'
    table_name = 'disfluencies'

    def __init__(self):
        super(Disfluencies, self).__init__()
        self._set_metrics_from_module(__name__)
