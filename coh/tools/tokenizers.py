# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division
import nltk
from nltk.data import load

#senter = load(base_path + '/models/punkt/punkt-senter.pickle')
senter = load('tokenizers/punkt/portuguese.pickle')

word_tokenize = nltk.word_tokenize
