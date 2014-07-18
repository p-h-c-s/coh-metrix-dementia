# -*- coding: utf-8 -*-
from coh import base
from coh.resource_pool import rp as default_rp
from itertools import chain


class ContentWordsFrequency(base.Metric):
    """"""
    def __init__(self, name='Content words frequency',
                 column_name='cw_freq'):
        super(ContentWordsFrequency, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp):
        frequencies = list(chain.from_iterable(rp.cw_freq(t)))

        return sum(frequencies) / len(frequencies)


class MinimumContentWordsFrequency(base.Metric):
    """"""
    def __init__(self, name='Minimum among content words frequencies',
                 column_name='min_cw_freq'):
        super(MinimumContentWordsFrequency, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp):
        frequencies = rp.cw_freq(t)
        min_freqs = [min(f) for f in frequencies]

        return sum(min_freqs) / len(min_freqs)


class Frequencies(base.Category):
    """
    """
    def __init__(self, name='Content word frequencies',
                 table_name='cw_frequencies'):
        super(Frequencies, self).__init__(name, table_name)
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(Frequencies, self).values_for_text(t, rp)
