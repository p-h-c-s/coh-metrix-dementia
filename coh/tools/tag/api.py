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


class Tagger(object):
    """Represents an interface for classes that perform part-of-speech tagging.

    There are two basic methods:
        tag: takes as input a list of tokens and return a list of tuples
        (string, string), containing the token and its PoS tag.

        batch_tag: takes as input a list of tokenized sentences and analyze
        them all at once.

    Derived classes must override at least one these methods. This class is
    based on nltk.tag.api.TaggerI
    (see http://www.nltk.org/api/nltk.tag.html#nltk.tag.api.TaggerI).
    """

    def tag(self, tokens):
        """Assign a part-of-speech tag to a tokenized sentence.

        Required parameters:
        tokens -- a list of strings, containing the tokens to be analyzed.

        Returns:
        A list of pairs (string, string), where the first string is the token
            and the second one is the corresponding PoS tag.
        """
        return self.tag_sents([tokens])[0]

    def tag_sents(self, sentences):
        """Assign part-of-speech tags to multiple sentences at once.

        Required parameters:
        sentences -- A list of lists of strings, containing the tokens to
            be analyzed, separated by sentences.

        Returns:
        A list of lists of pairs (string, string), one list of each sentence.
        """
        return [self.tag(sent) for sent in sentences]


class TagSet(object):
    """Represents a set of tags used by a tagger. This class is entended to
    facilitate the use of multiple taggers with different tagsets.

    Subclasses must, at least, define the *_tags lists.
    """
    article_tags = []
    verb_tags = []
    auxiliary_verb_tags = []
    participle_tags = []
    noun_tags = []
    adjective_tags = []
    adverb_tags = []
    pronoun_tags = []
    numeral_tags = []
    conjunction_tags = []
    preposition_tags = []
    interjection_tags = []
    currency_tags = []

    content_word_tags = []
    function_word_tags = []

    functions_as_noun_tags = []
    functions_as_adjective_tags = []

    punctuation_tags = []

    def __init__(self):
        """Form a TagSet.

            This function will look at the attributes ending with '_tags' and
            generate proper helping methods, that return True if the given tag
            is in the list, and False otherwise. If an attribute is of the form
            'functions_as_foo_tags', __init__ will generate a method called
            'functions_as_foo(tag)'; otherwise, if it's of the form 'foo_tags',
            it will generate a method called 'is_foo(tag)'.
        """
        n = len('_tags')

        for attr in dir(self):
            if attr.endswith('_tags'):
                if attr.startswith('functions_as'):
                    setattr(self, attr[:-n],
                            lambda tag: tag in getattr(self, attr))
                else:
                    setattr(self, 'is_' + attr[:-n],
                            lambda tag: tag in getattr(self, attr))
