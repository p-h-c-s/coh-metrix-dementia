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
import warnings
from itertools import chain
from coh.tools import senter, word_tokenize,\
    pos_tagger, stemmer, parser, dep_parser, univ_pos_tagger
from coh.utils import is_valid_id
from coh.database import create_engine, create_session, Helper


class ResourcePool(object):
    """A resource pool is a repository of methods for producing application
    resources. It centralizes tasks like PoS-tagging and sentence splitting,
    allowing synchronization among threads and use of multiple tools for
    the same task (e.g., taggers). It also allows the creation and reuse of
    database connections and similar resources.
    """
    def __init__(self, debug=False):
        """Form a new resource pool."""
        # The resources, in the form {<suffix> : <hook>}.
        self._res = {}
        # Resources already asked for, in the form
        # {(<text>, <suffix>) : <data>}.
        self._cache = {}
        self._debug = debug

    def register(self, suffix, hook):
        """Register a new resource.

        :suffix: A string identifying the resource type.
        :hook: The method that, when called, generates the resource data.
        :returns: None.

        """
        if suffix in self._res:
            warnings.warn("Resource \"{0}\" already registered.".format(suffix))

        self._res[suffix] = hook
        if is_valid_id(suffix):
            setattr(self, suffix, lambda *args: self.get(suffix, *args))

    def get(self, suffix, *args):
        """Get a resource.

        :suffix: The type of the resource to be extracted.
        :args: (Optional) arguments to be passed to the resource's hook.
        :returns: The resource data (as returned by the resource's hook.)

        """
        res_id = (suffix, ) + args

        if suffix not in self._res:
            raise ValueError('Resource \"{0}\" not registered.'.format(suffix))

        if res_id not in self._cache:
            self._cache[res_id] = self._res[suffix](*args)

            if self._debug:
                print('ResourcePool: calculated resource', res_id)

        return self._cache[res_id]


class DefaultResourcePool(ResourcePool):
    """A resource pool that uses the standard tools.
    """
    def __init__(self, debug=False):
        """Registers the default resources."""
        super(DefaultResourcePool, self).__init__(debug)

        # Tools and helpers.
        self.register('pos_tagger', lambda: pos_tagger)
        self.register('univ_pos_tagger', lambda: univ_pos_tagger)
        self.register('parser', lambda: parser)
        self.register('dep_parser', lambda: dep_parser)
        self.register('stemmer', lambda: stemmer)
        self.register('db_helper', self._db_helper)

        # Basic text info.
        self.register('paragraphs', lambda t: t.paragraphs)
        self.register('sentences', self._sentences)
        self.register('tokens', self._tokens)
        self.register('all_tokens', self._all_tokens)
        self.register('all_words', self._all_words)
        self.register('tagged_sentences', self._tagged_sentences)
        self.register('tagged_tokens', self._tagged_tokens)
        self.register('tagged_words', self._tagged_words)

        # Derived text info.
        self.register('content_words', self._content_words)
        self.register('stemmed_content_words', self._stemmed_content_words)
        self.register('cw_freq', self._cw_freq)
        self.register('token_types', self._token_types)

        # Parse structures.
        self.register('parse_trees', self._parse_trees)
        self.register('dep_trees', self._dep_trees)

    def _db_helper(self):
        """Creates a database session and returns a Helper associated with it.
        """
        engine = create_engine()
        session = create_session(engine)
        helper = Helper(session)

        return helper

    def _sentences(self, text):
        """Return a list of strings, each one being a sentence of the text.
        """
        paragraphs = self.get('paragraphs', text)
        sentences = chain.from_iterable(
            [senter.tokenize(p) for p in paragraphs])
        return list(sentences)

    def _tokens(self, text):
        """Return a list of lists of strings, where each list of strings
            corresponds to a sentence, and each string in the list is a token.
        """
        sentences = self.get('sentences', text)
        return list([word_tokenize(sent) for sent in sentences])

    def _all_tokens(self, text):
        """Return all tokens of the text in a single list.
        """
        tokens = self.get('tokens', text)
        return list(chain.from_iterable(tokens))

    def _all_words(self, text):
        """Return all non-punctuation tokens of the text in a single list.
        """
        tagged_words = self.get('tagged_words', text)
        return [word[0] for word in tagged_words]

    def _tagged_sentences(self, text):
        """Return a list of lists of pairs (string, string), representing
            the sentences with tagged tokens.
        """
        tokens = self.get('tokens', text)
        return pos_tagger.tag_sents(tokens)

    def _tagged_tokens(self, text):
        """Return a list of pair (string, string), representing the tokens
            not separated in sentences.
        """
        tagged_sentences = self.get('tagged_sentences', text)
        return list(chain.from_iterable(tagged_sentences))

    def _tagged_words(self, text):
        """Return a list of pair (string, string), representing the
            non-punctuation tokens not separated in sentences.
        """
        tagged_tokens = self.get('tagged_tokens', text)
        tagset = self.get('pos_tagger').tagset
        tagged_words = [token for token in tagged_tokens
                        if not tagset.is_punctuation(token)]
        return tagged_words

    def _content_words(self, text):
        """Return the content words of the text, separated in sentences.

        :text: @todo
        :returns: @todo

        """
        tagged_sents = self.get('tagged_sentences', text)
        content_words = list(tagged_sents)
        for i in range(len(tagged_sents)):
            content_words[i] = [word for (word, tag) in tagged_sents[i]
                                if pos_tagger.tagset.is_content_word(
                                    (word, tag))]
        return content_words

    def _stemmed_content_words(self, text):
        """Return the stem of each content word in the text, separated in
            sentences.

        :text: @todo
        :returns: @todo

        """
        tagged_sents = self.get('tagged_sentences', text)
        tagset = self.get('pos_tagger').tagset
        stemmed_content_words = []
        stemmer = self.get('stemmer')
        for sentence in tagged_sents:

            curr_sentence = []
            for token in sentence:
                if tagset.is_content_word(token):
                    # TODO: add 'tag' to stemmer.get_lemma call after
                    #   tag normalization.
                    lemma = stemmer.get_lemma(token[0])
                    lemma = lemma if lemma else token[0]
                    curr_sentence.append(lemma)

            stemmed_content_words.append(curr_sentence)
            # stemmed_content_words[i] = [stemmer.get_lemma(word)
            #                             for (word, tag) in tagged_sents[i]
            #                             if pos_tagger.tagset.is_content_word(
            #                             (word, tag))]
        return stemmed_content_words

    def _cw_freq(self, text):
        """Return the frequency of each content word in the text, separated
        by sentences.

        :text: @todo
        :returns: @todo

        """
        content_words = self.get('content_words', text)
        db_helper = self.get('db_helper')
        frequencies = list(content_words)

        for i in range(len(frequencies)):
            frequencies[i] = [db_helper.get_frequency(word.lower())
                              for word in content_words[i]]
            frequencies[i] = [f.freq if f is not None else 0
                              for f in frequencies[i]]

        return frequencies

    def _token_types(self, text):
        """Return the token types of the text, as a set.

        :text: TODO
        :returns: TODO

        """
        words = [word.lower() for word in self.get('all_words', text)]
        return set(words)

    def _parse_trees(self, text):
        """Return the parse tree of each sentence in the text.

        :text: TODO
        :returns: TODO
        """
        tokens = self.get('tokens', text)
        sentences = [' '.join(sent) for sent in tokens]
        return parser.parse_sents(sentences)

    def _dep_trees(self, text):
        """Return the dependency tree of each sentence in the text.

        :text: TODO
        :returns: TODO
        """
        sents = self.get('tokens', text)
        return self.get('dep_parser').parse_sents(sents)


rp = DefaultResourcePool()
