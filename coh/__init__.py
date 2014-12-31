# -*- coding: utf-8 -*-
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

all_metrics = MetricsSet([BasicCounts(),
                          LogicOperators(),
                          Frequencies(),
                          Hypernyms(),
                          Tokens(),
                          Connectives(),
                          Ambiguity(),
                          ])


rp = DefaultResourcePool()


__all__ = sorted([m for m in locals().keys()
                  if not m.startswith('_')])
