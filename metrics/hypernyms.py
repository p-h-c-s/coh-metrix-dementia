# -*- coding: utf-8 -*-
from coh import base
from coh.resource_pool import rp as default_rp


class HypernymsVerbs(base.Metric):
    """"""
    def __init__(self, name='Mean hypernyms per verb',
                 column_name='hypernyms_verbs'):
        super(HypernymsVerbs, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        verb_tokens = [token[0] for token in rp.tagged_words(t)
                       if rp.pos_tagger().tagset.is_verb(token)]
        verbs = [rp.db_helper().get_delaf_verb(verb) for verb in verb_tokens]
        lemmas = [verb.lemma for verb in verbs if verb is not None]
        hyper = [rp.db_helper().get_hypernyms(lemma) for lemma in lemmas]
        hyper_levels = [lemma.hyper_levels for lemma in hyper
                        if lemma is not None]
        return sum(hyper_levels) / len(hyper_levels)


class Hypernyms(base.Category):
    """
    """
    def __init__(self, name='Hypernyms', table_name='hypernyms'):
        super(Hypernyms, self).__init__(name, table_name)
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(Hypernyms, self).values_for_text(t, rp)
