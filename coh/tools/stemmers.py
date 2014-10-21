# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import coh.resource_pool


class DelafStemmer(object):

    """Docstring for DelafStemmer. """

    def __init__(self):
        """@todo: to be defined1. """
        pass

    def get_lemma(self, word, pos=None):
        word = coh.resource_pool.rp.db_helper().get_delaf_word(word, pos)
        return word.lemma if word is not None else None
