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
from coh import base
from coh.resource_pool import rp as default_rp
from itertools import chain


class ContentWordsFrequency(base.Metric):
    """
    Frequência das palavras de conteúdo:

        Média de todas as frequências das palavras de conteúdo (substantivos,
        verbos, advérbios e adjetivos) encontradas no texto. O valor da
        frequência das palavras é retirado da lista de frequências do córpus
        Banco de Português (BP), compilado por Tony Sardinha da PUC-SP.

        Exemplo:

            "Acessório utilizado por adolescentes, o boné é um dos itens que
            compõem a vestimenta idealizada pela proposta."
    """
    name = 'Content words frequency'
    column_name = 'cw_freq'

    def value_for_text(self, t, rp=default_rp):
        frequencies = list(chain.from_iterable(rp.cw_freq(t)))

        return sum(frequencies) / len(frequencies) if frequencies else 0


class MinimumContentWordsFrequency(base.Metric):
    """
    Frequência da palavra de conteúdo mais rara:

        Primeiramente identificamos a menor frequência dentre todas as palavras
        de conteúdo (substantivos, verbos, advérbios e adjetivos) em cada
        sentença. Depois, calculamos uma média de todas as frequências mínimas.
        A palavra com a menor frequência é a mais rara da sentença.
    """
    name = 'Minimum among content words frequencies'
    column_name = 'min_cw_freq'

    def value_for_text(self, t, rp=default_rp):
        frequencies = rp.cw_freq(t)
        # TODO: Check the len(f) > 0 (not a problem in Python 3!)
        min_freqs = [min(f) for f in frequencies if len(f) > 0]

        return sum(min_freqs) / len(min_freqs) if min_freqs else 0


class Frequencies(base.Category):
    """
    """
    name = 'Content word frequencies'
    table_name = 'cw_frequencies'

    def __init__(self):
        super(Frequencies, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(Frequencies, self).values_for_text(t, rp)
