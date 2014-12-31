# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from coh import base
from coh.resource_pool import rp as default_rp


class IdeaDensity(base.Metric):
    name = 'Idea Density'
    column_name = 'idea_density'

    def value_for_text(self, t, rp=default_rp):
        pass


class ContentDensity(base.Metric):
    name = 'Content Density'
    column_name = 'content_density'

    def value_for_text(self, t, rp=default_rp):
        pass


class SemanticDensity(base.Category):
    name = 'Semantic Density'
    table_name = 'semantic_density'

    def __init__(self):
        super(SemanticDensity, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
