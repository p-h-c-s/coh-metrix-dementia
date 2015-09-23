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


class HypernymsVerbs(base.Metric):
    """
        ## Hiperônimos de Verbos:

        Para cada verbo soma-se o número de hiperônimos e divide o total pelo
        número de verbos. Hiperonímia é uma relação, definida na Wordnet.Br
        (Dias-da-Silva et. al., 2002; Dias-da-Silva, 2003; Dias-da-Silva, 2005;
        Dias-da-Silva et. al., 2008 e Scarton e Aluísio, 2009), de "super tipo
        de". O verbo sonhar, por exemplo, possui 3 hiperônimos: imaginar,
        conceber e ver na mente.

        O desempenho da métrica é diretamente relacionado ao desempenho da
        base Wordnet.Br.

        ### Exemplo:

        *"Ele sonha muito quando está acordado."*

        O verbo sonhar possui 3 hiperônimos e o verbo acordar nenhum.
            Assim, temos o valor de 1,5.
    """

    name = 'Mean hypernyms per verb'
    column_name = 'hypernyms_verbs'

    def value_for_text(self, t, rp=default_rp, ignore_pos=False):
        verb_tokens = [token[0] for token in rp.tagged_words(t)
                       if rp.pos_tagger().tagset.is_verb(token)
                       or rp.pos_tagger().tagset.is_auxiliary_verb(token)
                       or rp.pos_tagger().tagset.is_participle(token)]
        verbs = [rp.db_helper().get_delaf_verb(verb) for verb in verb_tokens]
        lemmas = [verb.lemma for verb in verbs if verb is not None]
        hyper = [rp.db_helper().get_hypernyms(lemma) for lemma in lemmas]
        hyper_levels = [lemma.hyper_levels for lemma in hyper
                        if lemma is not None]
        return sum(hyper_levels) / len(hyper_levels) if hyper_levels else 0


class Hypernyms(base.Category):
    """
    """
    name = 'Hypernyms'
    table_name = 'hypernyms'

    def __init__(self):
        super(Hypernyms, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(Hypernyms, self).values_for_text(t, rp)
