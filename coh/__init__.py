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

from coh.base import (
    Text,
    Category,
    Metric,
    MetricsSet,
    ResultSet,
)

from coh.resource_pool import (
    ResourcePool,
    DefaultResourcePool,
    rp,
)

from coh.metrics import *
from coh.tools import *
from coh.conf import config

# XXX: this is obsolete. It will be removed in future versions.
# It's here only for back compatibility.
all_metrics = MetricsSet([BasicCounts(),
                          LogicOperators(),
                          Frequencies(),
                          Hypernyms(),
                          Tokens(),
                          Connectives(),
                          Ambiguity(),
                          # SyntacticalComplexity(),
                          # SemanticDensity(),
                          Constituents(),
                          Anaphoras(),
                          Coreference(),
                          # Lsa(),
                          # Disfluencies(),
                          ])


ALL_METRICS = MetricsSet([BasicCounts(),
                          LogicOperators(),
                          Frequencies(),
                          Hypernyms(),
                          Tokens(),
                          Connectives(),
                          Ambiguity(),
                          SyntacticalComplexity(),
                          Category([ContentDensity(),],
                                   name='SemanticDensity',
                                   table_name='semantic_density'),
                          Constituents(),
                          Anaphoras(),
                          Coreference(),
                          Lsa(),
                          Disfluencies(),
                         ])


CMP_METRICS = MetricsSet([BasicCounts(),
                          LogicOperators(),
                          Frequencies(),
                          Hypernyms(),
                          Category([PersonalPronounsIncidence(),
                                    PronounsPerNounPhrase(),
                                    TypeTokenRatio()],
                                   name='Tokens',
                                   table_name="tokens"),
                          Constituents(),
                          Connectives(),
                          Ambiguity(),
                          Coreference(),
                          Anaphoras(),
                         ])


NEW_METRICS = MetricsSet([Category([BrunetIndex(),
                                    HoroneStatistic(),
                                    MeanClauseSentence(),
                                   ],
                                   name='Tokens',
                                   table_name="tokens"),
                          SyntacticalComplexity(),
                          Category([ContentDensity(),],
                                   name='Semantic Density',
                                   table_name='semantic_density'),
                          Lsa(),
                          Disfluencies(),
                         ])


rp = DefaultResourcePool()


__all__ = sorted([m for m in locals().keys()
                  if not m.startswith('_')])
