# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
from coh import base
from coh.utils import ilen
from coh.tools import syllable_separator, pos_tagger
from coh.resource_pool import rp as default_rp
from itertools import chain


class Flesch(base.Metric):
    """
    """
    name = 'Flesch index'
    column_name = 'flesch'

    def value_for_text(self, t, rp=default_rp):
        mean_words_per_sentence = WordsPerSentence().value_for_text(t)

        syllables = chain.from_iterable(
            map(syllable_separator.separate, rp.all_words(t)))
        mean_syllables_per_word = ilen(syllables) / ilen(rp.all_words(t))

        flesch = 164.835 - 1.015 * mean_words_per_sentence\
            - 84.6 * mean_syllables_per_word

        return flesch


class Words(base.Metric):
    """
    """
    name = 'Number of Words'
    column_name = 'words'

    def value_for_text(self, t, rp=default_rp):
        # return ilen(filterfalse(pos_tagger.tagset.is_punctuation,
        #                         rp.tagged_words(t)))
        return len([w for w in rp.tagged_words(t)
                    if not pos_tagger.tagset.is_punctuation(w)])


class Sentences(base.Metric):
    """
    """
    name = 'Number of Sentences'
    column_name = 'sentences'

    def value_for_text(self, t, rp=default_rp):
        return ilen(rp.sentences(t))


class Paragraphs(base.Metric):
    """
    """
    name = 'Number of Paragraphs'
    column_name = 'paragraphs'

    def value_for_text(self, t, rp=default_rp):
        return ilen(rp.paragraphs(t))


class WordsPerSentence(base.Metric):
    """
    """
    name = 'Mean words per sentence'
    column_name = 'words_per_sentence'

    def value_for_text(self, t, rp=default_rp):
        return Words().value_for_text(t) / Sentences().value_for_text(t)


class SentencesPerParagraph(base.Metric):
    """
    """
    name = 'Mean sentences per paragraph'
    column_name = 'sentences_per_paragraph'

    def value_for_text(self, t, rp=default_rp):
        return Sentences().value_for_text(t) / Paragraphs().value_for_text(t)


class SyllablesPerContentWord(base.Metric):
    """
    """
    name = 'Mean syllables per content word'
    column_name = 'syllables_per_content_word'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word,
                                rp.tagged_words(t))
        content_words = map(lambda t: t[0], content_tokens)

        syllables = map(syllable_separator.separate, content_words)

        nwords = 0
        nsyllables = 0
        for w in syllables:
            nwords += 1
            nsyllables += len(w)

        return nsyllables / nwords


class VerbIncidence(base.Metric):
    """
    """
    name = 'Verb incidence'
    column_name = 'verbs'

    def value_for_text(self, t, rp=default_rp):
        verbs = filter(pos_tagger.tagset.is_verb, rp.tagged_words(t))
        return ilen(verbs) / ilen(rp.all_words(t))


class NounIncidence(base.Metric):
    """
    """
    name = 'Noun incidence'
    column_name = 'nouns'

    def value_for_text(self, t, rp=default_rp):
        nouns = filter(pos_tagger.tagset.is_noun, rp.tagged_words(t))
        return ilen(nouns) / ilen(rp.all_words(t))


class AdjectiveIncidence(base.Metric):
    """
    """
    name = 'Adjective incidence'
    column_name = 'adjectives'

    def value_for_text(self, t, rp=default_rp):
        adjectives = filter(pos_tagger.tagset.is_adjective, rp.tagged_words(t))
        return ilen(adjectives) / ilen(rp.all_words(t))


class AdverbIncidence(base.Metric):
    """
    """
    name = 'Adverb incidence'
    column_name = 'adverbs'

    def value_for_text(self, t, rp=default_rp):
        adverbs = filter(pos_tagger.tagset.is_adverb, rp.tagged_words(t))
        return ilen(adverbs) / ilen(rp.all_words(t))


class PronounIncidence(base.Metric):
    """
    """
    name = 'Pronoun incidence'
    column_name = 'pronouns'

    def value_for_text(self, t, rp=default_rp):
        pronouns = filter(pos_tagger.tagset.is_pronoun, rp.tagged_words(t))
        return ilen(pronouns) / ilen(rp.all_words(t))


class ContentWordIncidence(base.Metric):
    """
    """
    name = 'Content word incidence'
    column_name = 'content_words'

    def value_for_text(self, t, rp=default_rp):
        content_words = filter(pos_tagger.tagset.is_content_word,
                               rp.tagged_words(t))
        return ilen(content_words) / ilen(rp.all_words(t))


class FunctionWordIncidence(base.Metric):
    """
    """
    name = 'Function word incidence'
    column_name = 'function_words'

    def value_for_text(self, t, rp=default_rp):
        function_words = filter(pos_tagger.tagset.is_function_word,
                                rp.tagged_words(t))
        return ilen(function_words) / ilen(rp.all_words(t))


class BasicCounts(base.Category):
    name = 'Basic Counts'
    table_name = 'basic_counts'

    def __init__(self):
        super(BasicCounts, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(BasicCounts, self).values_for_text(t, rp)
