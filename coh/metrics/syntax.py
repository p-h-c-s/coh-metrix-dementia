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
from coh import base
from coh.resource_pool import rp as default_rp
from coh.utils import reverse_tree
from nltk.util import trigrams


class YngveComplexity(base.Metric):
    """
        ## Complexidade de Yngve
        
        Média da complexidade sintática de Yngve, descrita em:
        
        YNGVE, V. H. A Model and an Hypothesis for Language Structure.
        __Proceedings of the American Philosophical Society__, v. 104,
        p. 444–466, 1960.
        
        Para um dado texto, calcula-se a complexidade sintática de cada
        sentença, e então calcula-se a média desses valores. No cálculo
        da complexidade, utiliza-se a __média__ dos escores das palavras.
        
        As árvores sintáticas utilizadas são geradas pelo LX-Parser [1].
        
        [1] Silva, João, António Branco, Sérgio Castro e Ruben Reis.
        Out-of-the-Box Robust Parsing of Portuguese. In *Proceedings of the 9th
        International Conference on the Computational Processing of Portuguese
        (PROPOR'10)*, pp. 75–85.
        
        ### Exemplo:
        
        *Maria foi ao mercado. No mercado, comprou ovos e pão.* 
        
        No exemplo, a primeira sentença possui complexidade de Yngve 1,4,
        e a segunda, 2,0, para um valor total de (1,4 + 2,0) / 2 = 1,7.
    """

    name = 'Yngve Complexity'
    column_name = 'yngve'

    def value_for_text(self, t, rp=default_rp):
        syntax_trees = rp.parse_trees(t)

        sentence_indices = []
        for tree in syntax_trees:
            reverse_tree(tree)

            leaves = tree.leaves()

            word_indices = []
            for i in range(len(leaves)):
                word_indices.append(sum(tree.leaf_treeposition(i)))

            reverse_tree(tree)

            sentence_indices.append((sum(word_indices) / len(word_indices)))

        return sum(sentence_indices) / len(sentence_indices) \
                if sentence_indices else 0


class FrazierComplexity(base.Metric):
    """
        ## Complexidade de Frazier
        
        Média da complexidade sintática de Frazier, descrita em:
        
        FRAZIER, L. Syntactic Complexity. In: DOWTY, D. R.; KARTTUNEN,
        L.; ZWICKY, A. M. (Ed.). __Natural Language Parsing: Psychological,
        Computational, and Theoretical Perspectives__. Cambridge: Cambridge
        University Press, 1985. p. 129–189.
        
        Para um dado texto, calcula-se a complexidade sintática de cada
        sentença, e então calcula-se a média desses valores. No cálculo
        da complexidade, utiliza-se o __máximo da soma de trigramas__ dos
        escores das palavras.
        
        As árvores sintáticas utilizadas são geradas pelo LX-Parser [1].
        
        [1] Silva, João, António Branco, Sérgio Castro e Ruben Reis.
        Out-of-the-Box Robust Parsing of Portuguese. In *Proceedings of the 9th
        International Conference on the Computational Processing of Portuguese
        (PROPOR'10)*, pp. 75–85.
        
        ### Exemplo:
        
        *Maria foi ao mercado. No mercado, comprou ovos e pão.* 
        
        No exemplo, a primeira sentença possui complexidade de Frazier 6,0,
        e a segunda, 5,0, para um valor total de (6,0 + 5,0) / 2 = 5,5.
    """

    name = 'Frazier Complexity'
    column_name = 'frazier'

    def value_for_text(self, t, rp=default_rp):
        syntax_trees = rp.parse_trees(t)

        sentence_indices = []
        for tree in syntax_trees:
            if tree.label() == 'ROOT':
                tree = tree[0]

            leaves = tree.leaves()

            word_indices = [0] * len(leaves)
            for i in range(len(leaves)):
                ref_vector = tree.leaf_treeposition(i)

                j = -2
                while j >= -len(ref_vector) and ref_vector[j] == 0:
                    parent_index = len(ref_vector) + j
                    parent_node = tree[ref_vector[:parent_index]]

                    if rp.parser().tagset.is_sentence_node(parent_node):
                        word_indices[i] += 1.5
                    else:
                        word_indices[i] += 1

                    j -= 1

            if len(leaves) < 3:
                sentence_index = sum(word_indices)
            else:
                max_trigrams = 0
                for trigram in trigrams(word_indices):
                    if sum(trigram) > max_trigrams:
                        max_trigrams = sum(trigram)
                sentence_index = max_trigrams

            sentence_indices.append(sentence_index)

        return sum(sentence_indices) / len(sentence_indices) \
                if sentence_indices else 0


class DependencyDistance(base.Metric):
    """
        ## Distância de dependência
        
        Média da distância de dependência das sentenças de um texto. Para cada
        sentença do texto, a distância de dependência é calculada como a soma
        da distância entre as palavras associadas a cada relação de
        dependência.
        
        As árvores de dependência são extraídas pelo
        [MaltParser](http://www.maltparser.org/)
        
        ### Exemplo:
        
        *Maria foi ao mercado. No mercado, comprou ovos e pão.* 
        
        Para a primeira sentença do exemplo, as relações de dependência e suas
        respectivas distâncias associadas são:
        
        1. nsubj(foi, Maria), 1
        2. adpmod(foi, ao), 1
        3. adpobj(ao, mercado), 1
        
        Para esta sentença, a distância de dependência é 3. Para a segunda
        sentença, as relações de dependência são:
        
        1. adpmod(comprou, No), 2
        2. adpobj(No, mercado), 1
        3. dobj(comprou, ovos), 1
        4. cc(ovos, e), 1
        5. conj(ovos, pão), 2
        
        Para esta sentença, a distância de dependência é 7. Portanto, para o
        exemplo todo, o valor da métrica será (3 + 7) / 2 = 5,0.
    """

    name = 'Dependency Distance'
    column_name = 'dep_distance'

    def value_for_text(self, t, rp=default_rp):
        graphs = rp.dep_trees(t)

        dep_distances = []
        for graph in graphs:
            dep_distance = 0
            for dep in graph.nodes.values():
                if dep['rel'] not in ('TOP', 'ROOT', 'p', 'root', 'punct'):
                    dep_distance += abs(dep['address'] - dep['head'])
                    # The 'ROOT' and 'p' tags are the ones returned by
                    # MaltParser, not 'root' and 'punct', but they stay to
                    # avoid breaking anything
            dep_distances.append(dep_distance)

        return sum(dep_distances) / len(dep_distances) \
                if dep_distances else 0


class CrossEntropy(base.Metric):
    """
        ## Entropia Cruzada
        
        Média da entropia cruzadas das sentenças do texto. A entropia
        cruzada mede o nível de "surpresa" do modelo de língua diante
        da sentença. Valores maiores de entropia cruzada significam que
        a sentença possui combinações não usuais de palavras. Tipicamente,
        portanto, quanto maior a entropia cruzada de uma sentença, maior sua
        complexidade esperada.
        
        Na versão atual do sistema, a entropia é calculada com base em um
        modelo de trigramas, treinado sobre um corpus de 120.813.620
        *tokens*, que consiste na união dos corpora: Wikipedia, PLN-BR,
        LácioWeb, e Revista Pesquisa FAPESP.
        
        ## Exemplo:
        
        *Maria foi ao mercado. No mercado, comprou ovos e pão.* 
        
        Para o exemplo, a entropia cruzada da primeira sentença, segundo
        o modelo, é 0,90, e a da segunda sentença, 0,91. Portanto, o valor
        da métrica para o texto é (0,90 + 0,91) / 2 = 0,905.
    """

    name = 'Cross Entropy'
    column_name = 'cross_entropy'

    def value_for_text(self, t, rp=default_rp):
        lm = rp.language_model()

        sents = [lm.clean(sent) for sent in rp.sentences(t)]
        scores = [-1/len(sent) * lm.score(sent) for sent in sents]

        return sum(scores) / len(scores) if scores else 0


class SyntacticalComplexity(base.Category):
    """Docstring for SyntacticalComplexity. """

    name = 'Syntactical Complexity'
    table_name = 'syntax'

    def __init__(self):
        super(SyntacticalComplexity, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)
