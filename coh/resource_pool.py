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
import re
import logging
from itertools import chain
from coh.tools import senter, word_tokenize,\
    pos_tagger, stemmer, parser, dep_parser, univ_pos_tagger
from coh.tools.lsa import LsaSpace
from coh.tools.lm import KenLmLanguageModel
from coh.utils import is_valid_id
from coh.database import create_engine, create_session, Helper
from coh.conf import config

import nltk


logger = logging.getLogger(__name__)


class ResourcePool(object):
    """A resource pool is a repository of methods for producing application
    resources. It centralizes tasks like PoS-tagging and sentence splitting,
    allowing synchronization among threads and use of multiple tools for
    the same task (e.g., taggers). It also allows the creation and reuse of
    database connections and similar resources.
    """

    def __init__(self, cache_limit=300):
        """Form a new resource pool.
        
        Optional arguments:
        :cache_limit: maximum number of unpinned items in the cache.
        """

        if cache_limit < 0:
            raise ValueError('Invalid cache limit %d. Must be >= 0.' % cache_limit)

        # The resource hooks, in the form {<suffix> : <hook>}.
        self._hooks = {}

        # Resources already asked for, in the form
        # [(<suffix>, <args>, <data>)].

        self._unpinned_cache = []
        self._pinned_cache = []

        self._pinned = set()
        self._cache_limit = cache_limit

    def register(self, suffix, hook, pinned=False):
        """Register a new resource.

        Required arguments:
        :suffix: A string identifying the resource type.
        :hook: The method that, when called, generates the resource data.

        Optional arguments:
        :pinned: True if the resource should be pinned in the cache.

        :returns: None.
        """

        if suffix in self._hooks:
            logger.warning("Resource \"%s\" already registered.", suffix)
        
        if pinned:
            self._pinned.add(suffix)

        self._hooks[suffix] = hook
        if is_valid_id(suffix):
            setattr(self, suffix, lambda *args: self.get(suffix, *args))

    @staticmethod
    def _get_index(cache, suffix, args):
        """Return the index of the element in the cache,
        or None if not present."""

        for i, elem in enumerate(cache):
            if elem[0] == suffix and elem[1] == args:
                return i
        return None

    def get(self, suffix, *args):
        """Get a resource.

        Required arguments:
        :suffix: The type of the resource to be extracted.
        :args: (Optional) arguments to be passed to the resource's hook.

        :returns: The resource data (as returned by the resource's hook.)
        """

        if suffix not in self._hooks:
            raise ValueError('Resource \"{0}\" not registered.'.format(suffix))

        if suffix in self._pinned:
            index = self._get_index(self._pinned_cache, suffix, args)
            if index is None:
                self._pinned_cache.append((suffix, args, self._hooks[suffix](*args)))
                index = len(self._pinned_cache) - 1

            return self._pinned_cache[index][2]
        else:
            index = self._get_index(self._unpinned_cache, suffix, args)
            if index is None:
                self._unpinned_cache.append((suffix, args, self._hooks[suffix](*args)))
                index = len(self._unpinned_cache) - 1
            value = self._unpinned_cache[index][2]

            if len(self._unpinned_cache) > self._cache_limit:
                del self._unpinned_cache[0]

            return value


class DefaultResourcePool(ResourcePool):
    """A resource pool that uses the standard tools.
    """
    def __init__(self):
        """Registers the default resources."""
        super(DefaultResourcePool, self).__init__()

        # Tools and helpers.
        self.register('pos_tagger', lambda: pos_tagger, pinned=True)
        self.register('univ_pos_tagger', lambda: univ_pos_tagger, pinned=True)
        self.register('parser', lambda: parser, pinned=True)
        self.register('dep_parser', lambda: dep_parser, pinned=True)
        self.register('stemmer', lambda: stemmer, pinned=True)
        self.register('db_helper', self._db_helper, pinned=True)
        self.register('idd3_engine', self._idd3_engine, pinned=True)

        # Basic text info.
        # TODO: these methods need renaming for better readability.
        self.register('raw_content', lambda t: t.raw_content)
        self.register('raw_words', self._raw_words)
        self.register('paragraphs', lambda t: t.paragraphs)
        self.register('sentences', self._sentences)
        self.register('tokens', self._tokens)
        self.register('all_tokens', self._all_tokens)
        self.register('all_words', self._all_words)
        self.register('tagged_sentences', self._tagged_sentences)
        self.register('tagged_tokens', self._tagged_tokens)
        self.register('tagged_words', self._tagged_words)
        self.register('tagged_words_in_sents', self._tagged_words_in_sents)

        # Derived text info.
        self.register('content_words', self._content_words)
        self.register('stemmed_content_words', self._stemmed_content_words)
        self.register('cw_freq', self._cw_freq)
        self.register('token_types', self._token_types)

        # Parse structures.
        self.register('parse_trees', self._parse_trees)
        self.register('dep_trees', self._dep_trees)

        self.register('toplevel_nps_per_sentence', self._toplevel_nps_per_sentence)
        self.register('leaves_in_toplevel_nps', self._leaves_in_toplevel_nps)

        # LSA spaces
        self.register('lsa_space', self._lsa_space, pinned=True)

        # Language models
        self.register('language_model', self._language_model, pinned=True)

    def _db_helper(self):
        """Creates a database session and returns a Helper associated with it.
        """
        engine = create_engine()
        session = create_session(engine)
        helper = Helper(session)

        return helper
    
    def _idd3_engine(self):
        """Create an IDD3 Engine, configure it, and return it.
        """
        import idd3
        from idd3.rules import pt

        idd3.use_language(pt)

        engine = idd3.Engine(idd3.all_rulesets, idd3.all_transformations)

        return engine

    def _raw_words(self, text):
        """TODO: Docstring for raw_words.

        :text: TODO
        :returns: TODO

        """

        clean_patterns = [re.compile(r'\(\([\w\d\s]*\)\)'),  # Metainfo
                          re.compile(r'\.\.\.'),  # Short pauses
                          re.compile(r'::+'),  # Vowel stretching
                          ]
        split_pattern = re.compile('\s+')

        content = text.raw_content
        for clean_pattern in clean_patterns:
            content = re.sub(clean_pattern, ' ', content)

        content = re.sub(split_pattern, ' ', content)

        return [word for word in content.split(' ') if word]

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
        """Return a list of pairs (string, string), representing the
            non-punctuation tokens not separated in sentences.
        """
        tagged_tokens = self.get('tagged_tokens', text)
        tagset = self.get('pos_tagger').tagset
        tagged_words = [token for token in tagged_tokens
                        if not tagset.is_punctuation(token)]
        return tagged_words

    def _tagged_words_in_sents(self, text):
        """Return a list of lists of pairs (string, string),
            representing the non-punctuation tokens separated
            in sentences.
        """
        tagged_sents = self.get('tagged_sentences', text)
        tagset = self.get('pos_tagger').tagset
        tagged_words = [[token for token in tagged_sent
                         if not tagset.is_punctuation(token)]
                        for tagged_sent in tagged_sents]
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

    def _toplevel_nps_per_sentence(self, text):
        """
        Returns the NPs that are not contained in any other NP
        in the parse tree for each sentence.

        This depends on the LX-Parser syntax tree.
        
        :rtype: List[List[nltk.Tree]].
        """
        def toplevel_nps(tree):
            """
            Generator over the NPs that are not contained in any
            other NP in the parse tree.
            """
            if tree.label() == 'NP':
                yield tree
            else:
                for child in tree:
                    if isinstance(child, nltk.Tree):
                        yield from toplevel_nps(child)
        parse_trees = self.get('parse_trees', text)
        return [list(toplevel_nps(tree)) for tree in parse_trees]

    def _leaves_in_toplevel_nps(self, text):
        """
        Get the leaves of the toplevel NPs, ignoring all punctuation, for each
        sentence.

        :rtype: List[List[List[str]]].
        """
        def extract_leaves(toplevel):
            """Given a toplevel NP, extract the leaves that are not punctuation"""
            leaves = toplevel.subtrees(lambda t: t.label() != 'PNT' and t.height() == 2)
            return [l[0] for l in leaves]
        return [[extract_leaves(toplevel) for toplevel in toplevels_in_sentence]
                for toplevels_in_sentence in self.get('toplevel_nps_per_sentence', text)]

    def _lsa_space(self):
        """Return the default LSA space.

        :returns: an LsaSpace.
        """
        space = LsaSpace(config['LSA_DICT_PATH'], config['LSA_MODEL_PATH'])
        return space
    
    def _language_model(self):
        """Return the default language model (a 3-gram model
        generated using KenLM).

        :returns: a kenlm.LanguageModel.
        """
        model = KenLmLanguageModel(config['KENLM_LANGUAGE_MODEL'])
        return model


rp = DefaultResourcePool()
