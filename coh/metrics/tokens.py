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
from coh.utils import find_subtrees
from collections import Counter
from math import log


class PersonalPronounsIncidence(base.Metric):
    """
        ## Incidência de Pronomes Pessoais:

        Incidência de pronomes pessoais em um texto. Consideramos como pronomes
        pessoais: eu, tu, ele/ela, nós, nós, eles/elas, você e vocês.

        ### Exemplo:

        *"O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."*

        Este exemplo possui 1 pronome pessoal. Como este texto possui 95
            palavras, a incidência de pronomes pessoais é 10,526 (número de
            pronomes pessoais/(número de palavras/1000)).
    """

    name = 'Personal pronouns incidence'
    column_name = 'personal_pronouns'

    personal_pronouns = ['eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles',
                         'elas', 'você', 'vocês']

    def __init__(self):
        super(PersonalPronounsIncidence, self).__init__()

    def value_for_text(self, t, rp=default_rp):
        words = [word.lower() for word in rp.all_words(t)]
        n_personal_pronouns = sum([word in self.personal_pronouns
                                   for word in words])
        return n_personal_pronouns / (len(words) / 1000) \
            if words else 0


class PronounsPerNounPhrase(base.Metric):
    """
        ## Pronomes por Sintagmas:

        Média do número de pronomes que aparecem em um texto pelo número de
        sintagmas nominais.

        O desempenho dessa métrica é diretamente relacionado ao desempenho das
        árvores sintáticas de constituintes geradas pelo LX-Parser.

        ### Exemplo:

        *"Dentro do lago, existem peixes, como a traíra e o dourado, além da
            palometa, um tipo de piranha. Ela é uma espécie carnívora que se
            alimenta de peixes."*

        Não há pronomes na primeira sentença e há 9 sintagmas nominais. Há
            1 pronome na segunda sentença e 5 sintagmas nominais. Com 1 pronome
            em 2 sentenças, o valor da métrica é 0,1.
    """

    name = 'Mean pronouns per noun phrase'
    column_name = 'pronouns_per_np'

    def value_for_text(self, t, rp=default_rp):
        parse_trees = rp.parse_trees(t)

        sent_indices = []
        for i, tree in enumerate(parse_trees):
            nps = 0
            prons = 0

            for np in find_subtrees(tree, 'NP'):
                prons += len([tt for tt in np
                              if tt.label() in ('PRS')])
                nps += 1

            sent_indices.append(prons / nps)

        return sum(sent_indices) / len(sent_indices) \
            if sent_indices else 0


class TypeTokenRatio(base.Metric):
    """
        ## Relação Tipo por Token:

        Número de palavras únicas dividido pelo número de tokens dessas
        palavras. Cada palavra única é um tipo. Cada instância desta palavra é
        um token.

        Por exemplo, se a palavra cachorro aparece 7 vezes em um texto, seu
        tipo (type) é 1 e seu token é 7.
        Calculamos esta métrica somente para palavras de conteúdo
        (substantivos, verbos, advérbios e adjetivos).

        Observação: Não usamos lematização de palavras, ou seja, a palavra
        cachorro é considerada diferente de cachorros.

        ### Exemplo:

        *"O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."*

        Com 95 tokens e 78 tipos, a relação tipo por token é 0,821.
    """

    name = 'Type to token ratio'
    column_name = 'ttr'

    def __init__(self):
        super(TypeTokenRatio, self).__init__()

    def value_for_text(self, t, rp=default_rp):
        tokens = rp.all_words(t)
        types = rp.token_types(t)

        ttr = len(types) / len(tokens) if tokens else 0

        return ttr


class BrunetIndex(base.Metric):
    """
        # Índice de Brunet:

            W = N ** (V ** −0.165)

        N é o número de palavras lexicais, e V é o número total de tokens
        usados.
        Os valores de W típicos variam entre 10 e 20, sendo que uma fala mais
        rica produz valores menores (THOMAS et al., 2005).

        ### Exemplo:

        *"O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."*

        Com 95 tokens e 78 tipos, a métrica vale 9,199.
    """

    name = 'Brunet Index'
    column_name = 'brunet'

    def value_for_text(self, t, rp=default_rp):
        tokens = rp.all_words(t)
        types = rp.token_types(t)

        brunet_index = len(tokens) ** len(types) ** -0.165

        return brunet_index


class HoroneStatistic(base.Metric):
    """
        ## Estatística de Horoné:

        A Estatística de Honoré R (HONORÉ, 1979), calculada como
        (THOMAS et al., 2005):

            R = 100 * logN / (1 - (V_1 / V))

        em que N é o número total de tokens, V_1 é o número de palavras do
        vocabulário que aparecem uma única vez, e V é o número de palavras
        lexicais.

        ### Exemplo:

        *"O acessório polêmico entrou no projeto, de autoria do senador
            Cícero Lucena (PSDB-PB), graças a uma emenda aprovada na Comissão
            de Educação do Senado em outubro. Foi o senador Flávio Arns (PT-PR)
            quem sugeriu a inclusão da peça entre os itens do uniforme de
            alunos dos ensinos Fundamental e Médio nas escolas municipais,
            estaduais e federais. Ele defende a medida como forma de proteger
            crianças e adolescentes dos males provocados pelo excesso de
            exposição aos raios solares. Se a idéia for aprovada, os estudantes
            receberão dois conjuntos anuais, completados por calçado, meias,
            calça e camiseta."*

        Com 95 tokens, 69 tokens com apenas uma ocorrência e 78 tipos, o
            valor da métrica é 1714,027.
    """

    name = 'Honore Statistic'
    column_name = 'honore'

    def value_for_text(self, t, rp=default_rp):
        tokens = [word.lower() for word in rp.all_words(t)]
        types = rp.token_types(t)

        counter = Counter(tokens)
        one_time_tokens = [word for word, count in counter.items()
                           if count == 1]

        honore_index = 100 * log(len(tokens), 10) /\
            (1 - len(one_time_tokens) / len(types))

        return honore_index


class MeanClauseSentence(base.Metric):
    """
        ## Cláusulas por Sentença:

        Calcula o número médio de cláusulas por sentença. Definiu-se que uma
        cláusula em uma sentença é caracterizada pela presença de um sintagma
        verbal.

        ### Exemplo:

        *"A mulher que eu vi usava um chapéu vermelho. O seu chapéu era
            muito bonito."*

        A primeira sentença possui 2 cláusulas e a segunda sentença possui
            uma cláusula. Assim, o valor da métrica é 1,5.
    """

    name = 'Mean Clauses per Sentence'
    column_name = 'mcu'

    def value_for_text(self, t, rp=default_rp):
        # We estimate the number of clauses by the number of S nodes in
        # the syntax tree that have a VP node.
        trees = rp.parse_trees(t)

        clauses = []
        for tree in trees:
            n_clauses = 0
            for subtree in tree.subtrees(lambda t: t.height() >= 3):
                if subtree.label() == 'S':
                    sub_vps = [t for t in subtree if t.label() == 'VP']
                    n_clauses += len(sub_vps)
            clauses.append(n_clauses)

        return sum(clauses) / len(clauses)


class Tokens(base.Category):
    name = 'Pronouns, Types, and Tokens'
    table_name = 'tokens'

    def __init__(self):
        super(Tokens, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(Tokens, self).values_for_text(t, rp)
