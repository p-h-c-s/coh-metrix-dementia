# -*- coding: utf-8 -*-
from coh import base
from coh.resource_pool import rp as default_rp


class PersonalPronounsIncidence(base.Metric):
    """
    """
    personal_pronouns = ['eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
                         'você', 'vocês']

    def __init__(self, name='Personal pronouns incidence',
                 column_name='personal_pronouns'):
        super(PersonalPronounsIncidence, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp):
        words = [word.lower() for word in rp.all_words(t)]
        n_personal_pronouns = sum([word in self.personal_pronouns
                                   for word in words])
        return n_personal_pronouns / len(words)


class PronounsPerNounPhrase(base.Metric):

    """Docstring for PronounsPerNounPhrase. """

    def __init__(self, name='Mean pronouns per noun phrase',
                 column_name='pronouns_per_np'):
        super(PronounsPerNounPhrase, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp):
        raise NotImplementedError('Waiting for syntactic parser')


class TypeTokenRatio(base.Metric):

    """Docstring for TypeTokenRatio. """

    def __init__(self, name='Type to token ratio',
                 column_name='ttr'):
        super(TypeTokenRatio, self).__init__(name, column_name)

    def value_for_text(self, t, rp=default_rp):
        words = [word.lower() for word in rp.all_words(t)]
        return len(set(words)) / len(words)


class Tokens(base.Category):

    def __init__(self, name='Pronouns, Types and Tokens',
                 table_name='tokens'):
        super(Tokens, self).__init__(name, table_name)
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
        # TODO: remove when PronounsPerNounPhrase is ready.
        del self.metrics[0]

    def values_for_text(self, t, rp=default_rp):
        return super(Tokens, self).values_for_text(t, rp)
