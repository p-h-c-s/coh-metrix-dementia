"""Helper classes for using Statistical Language Models."""

# -*- coding: utf-8 -*-
# Coh-Metrix-Dementia - Automatic text analysis and classification for dementia.
# Copyright (C) 2014-2015  Andre Luiz Verucci da Cunha
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

import kenlm


class KenLmLanguageModel(object):
    """A class for interfacing with the KenLM toolkit."""

    def __init__(self, model_path):
        self.model = kenlm.LanguageModel(model_path)

    def score(self, sent):
        """Return the score assigned by the model to a sentence."""

        return self.model.score(sent)

    def clean(self, raw_sent):
        """Clean a sentence, so that it can be run
        through the model."""

        return raw_sent
