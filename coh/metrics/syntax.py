# -*- coding: utf-8 -*-
# Coh-Metrix-Dementia - Automatic text analysis and classification for dementia.
# Copyright (C) 2014-2015  Andre Luiz Verucci da Cunha
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
from coh.utils import reverse_tree


class YngveComplexity(base.Metric):

    """Docstring for YngveComplexity. """

    name = 'Yngve Complexity'
    column_name = 'yngve'

    def value_for_text(self, t, rp=default_rp):
        syntax_trees = rp.parse_trees(t)

        sentence_indices = []
        for tree in syntax_trees:
            reverse_tree(tree)

            leaves = tree.leaves()

            word_indices = []
            for i in range(len(leaves)):
                word_indices.append(sum(tree.leaf_treeposition(i)))

            reverse_tree(tree)

            sentence_indices.append((sum(word_indices) / len(word_indices)))

        return sum(sentence_indices) / len(sentence_indices)


class FrazierComplexity(base.Metric):

    """Docstring for FrazierComplexity. """

    name = 'Frazier Complexity'
    column_name = 'frazier'

    def value_for_text(self, t, rp=default_rp):
        pass


class DependencyDistance(base.Metric):

    """Docstring for DependencyDistance. """

    name = 'Dependency Distance'
    column_name = 'dep_distance'

    def value_for_text(self, t, rp=default_rp):
        pass


class CrossEntropy(base.Metric):

    """Docstring for CrossEntropy. """

    name = 'Cross Entropy'
    column_name = 'cross_entropy'

    def value_for_text(self, t, rp=default_rp):
        pass


class SyntacticalComplexity(base.Category):

    """Docstring for SyntacticalComplexity. """

    name = 'Syntactical Complexity'
    table_name = 'syntax'

    def __init__(self):
        super(SyntacticalComplexity, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
