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


class IdeaDensity(base.Metric):
    name = 'Idea Density'
    column_name = 'idea_density'

    def value_for_text(self, t, rp=default_rp):
        pass


class ContentDensity(base.Metric):

    """Docstring for HoroneIndex. """

    name = 'Content density'
    column_name = 'content_density'

    def value_for_text(self, t, rp=default_rp):
        tagged_words = rp.tagged_words(t)
        tagset = rp.pos_tagger().tagset

        content_words = [word for word in tagged_words
                         if tagset.is_content_word(word)]

        function_words = [word for word in tagged_words
                          if tagset.is_function_word(word)]

        content_density = len(content_words) / len(function_words)

        return content_density


class SemanticDensity(base.Category):
    name = 'Semantic Density'
    table_name = 'semantic_density'

    def __init__(self):
        super(SemanticDensity, self).__init__()
        # self._set_metrics_from_module(__name__)
        self.metrics = [ContentDensity(), ]
        self.metrics.sort(key=lambda m: m.name)
