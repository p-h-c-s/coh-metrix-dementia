# -*- coding: utf-8 -*-
import coh.resource_pool


class DelafStemmer(object):

    """Docstring for DelafStemmer. """

    def __init__(self):
        """@todo: to be defined1. """
        pass

    def get_lemma(self, verb):
        verb = coh.resource_pool.rp.db_helper().get_verb(verb)
        return verb.lemma if verb is not None else None
