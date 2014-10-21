# -*- coding: utf-8 -*-
from coh import base
from coh.resource_pool import rp as default_rp


def calculate_ambiguity(rp, t, delaf_tag, tep_tag, checker):
    """Calculates the ambiguity metric for a word category, which is the average
    number of meanings of the words belonging to this category in the text.

    :rp: the resource pool to be used.
    :t: the text to be analyzed.
    :delaf_tag: the corresponding PoS tag used in the DELAF tables.
    :tep_tag: the corresponding PoS tag used in the Tep tables.
    :checker: a function that returns True iff a token is of the desired
    category

    :returns: the ratio between the total number of meanings and the total
    number of words for a given category.

    """
    words = [word.lower() for (word, tag) in rp.tagged_words(t)
             if checker((word, tag))]

    word_stems = [rp.stemmer().get_lemma(word, delaf_tag) for word in words]
    word_stems = [word for word in word_stems if word is not None]

    meanings_count = [rp.db_helper().get_tep_words_count(stem, tep_tag)
                      for stem in word_stems]
    meanings_count = [m for m in meanings_count if m is not None]

    return sum(meanings_count) / len(words)


class VerbAmbiguity(base.Metric):
    """
    """
    name = 'Ambiguity of verbs'
    column_name = 'verbs'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'V', 'Verbo',
                                   rp.pos_tagger().tagset.is_verb)


class NounAmbiguity(base.Metric):
    """
    """
    name = 'Ambiguity of nouns'
    column_name = 'nouns'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'N', 'Substantivo',
                                   rp.pos_tagger().tagset.is_noun)


class AdjectiveAmbiguity(base.Metric):
    """
    """
    name = 'Ambiguity of adjectives'
    column_name = 'adjectives'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'A', 'Adjetivo',
                                   rp.pos_tagger().tagset.is_adjective)


class AdverbAmbiguity(base.Metric):
    """
    """
    name = 'Ambiguity of adverbs'
    column_name = 'adverbs'

    def value_for_text(self, t, rp=default_rp):
        return calculate_ambiguity(rp, t, 'ADV', 'Advérbio',
                                   rp.pos_tagger().tagset.is_adverb)


class Ambiguity(base.Category):
    name = 'Ambiguity'
    table_name = 'ambiguity'

    def __init__(self):
        super(Ambiguity, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
