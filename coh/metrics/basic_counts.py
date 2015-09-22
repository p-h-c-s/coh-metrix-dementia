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
from coh.utils import ilen
from coh.tools import syllable_separator, pos_tagger
from coh.resource_pool import rp as default_rp
from itertools import chain


class Flesch(base.Metric):
    """
        ## Índice Flesch:

        O Índice de Legibilidade de Flesch busca uma correlação entre tamanhos
        médios de palavras e sentenças e a facilidade de leitura.

        A adaptação do Índice Flesch da língua inglesa para a portuguesa foi
        realizada por Martins, Teresa B. F., Claudete M. Ghiraldelo, Maria das
        Graças Volpe Nunes e Osvaldo Novais de Oliveira Junior (1996).
        Readability formulas applied to textbooks in brazilian
portuguese. Notas do ICMC, N. 28, 11p.

        ### Fórmula:

        *ILF = 248.835 - [1.015 x (Número de palavras por sentença)] -
            [84.6 x (Número de sílabas do texto / Número de palavras do texto)]*

        ### Exemplo:

        *"Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça
            entre os itens do uniforme de alunos dos ensinos Fundamental e
            Médio nas escolas municipais, estaduais e federais. Ele defende a
            medida como forma de proteger crianças e adolescentes dos males
            provocados pelo excesso de exposição aos raios solares. Se a idéia
            for aprovada, os estudantes receberão dois conjuntos anuais,
            completados por calçado, meias, calça e camiseta."*

        Com média de 23 palavras por sentença e 2,31 sílabas por palavra,
            o índice Flesch para o exemplo é 29,316.

    """

    name = 'Flesch index'
    column_name = 'flesch'

    def value_for_text(self, t, rp=default_rp):
        mean_words_per_sentence = WordsPerSentence().value_for_text(t)

        syllables = chain.from_iterable(
            map(syllable_separator.separate, rp.all_words(t)))
        mean_syllables_per_word = ilen(syllables) / ilen(rp.all_words(t))

        flesch = 248.835 - 1.015 * mean_words_per_sentence\
            - 84.6 * mean_syllables_per_word

        return flesch


class Words(base.Metric):
    """
        ## Número de Palavras:

        Número de palavras do texto.

        ### Exemplo:

        *"Acessório utilizado por adolescentes, o boné é um dos itens que
            compõem a vestimenta idealizada pela proposta."*

        O exemplo possui 17 palavras.
    """

    name = 'Number of Words'
    column_name = 'words'

    def value_for_text(self, t, rp=default_rp):
        # return ilen(filterfalse(pos_tagger.tagset.is_punctuation,
        #                         rp.tagged_words(t)))
        return len(rp.tagged_words(t))


class Sentences(base.Metric):
    """
        ## Número de Sentenças:

        Número de sentenças de um texto.

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

        O exemplo possui 4 sentenças.
    """

    name = 'Number of Sentences'
    column_name = 'sentences'

    def value_for_text(self, t, rp=default_rp):
        return ilen(rp.sentences(t))


class Paragraphs(base.Metric):
    """
        ## Número de Parágrafos:

        Número de parágrafos de um texto. Consideramos como parágrafos somente
        a quebra de linha (não identações).

        ### Exemplo:

        *"No caso do Jeca Tatu, o verme que o deixou doente foi outro: o
            Ancylostoma. A larva desse verme vive no solo e penetra diretamente
            na pele. Só o contrai quem anda descalço na terra contaminada por
            fezes humanas. Se não se tratar, a pessoa fica fraca, sem ânimo e
            com a pele amarelada. Daí a doença ser também conhecida como
            amarelão.*

        *Os vermes – também chamados de helmintos – são parasitos, animais
            que, em geral, dependem da relação com outros seres para viver.
            Eles podem se hospedar no organismo de diversos animais, como bois,
            aves e peixes. Por isso, podemos também contraí-los comendo carnes
            cruas ou mal cozidas."*

        O exemplo possui 2 parágrafos.
    """

    name = 'Number of Paragraphs'
    column_name = 'paragraphs'

    def value_for_text(self, t, rp=default_rp):
        return ilen(rp.paragraphs(t))


class WordsPerSentence(base.Metric):
    """
        ## Palavras por Sentenças:

        Número de palavras dividido pelo número de sentenças.

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

        Neste exemplo o número de palavras é 95 e o número de sentenças é
            4. Portanto,o número de palavras por sentenças é 23,75.
    """

    name = 'Mean words per sentence'
    column_name = 'words_per_sentence'

    def value_for_text(self, t, rp=default_rp):
        return Words().value_for_text(t) / Sentences().value_for_text(t)


class SentencesPerParagraph(base.Metric):
    """
        ## Sentenças por Parágrafos:

        Número de sentenças dividido pelo número de parágrafos.

        ### Exemplo:

        *"No caso do Jeca Tatu, o verme que o deixou doente foi outro: o
            Ancylostoma. A larva desse verme vive no solo e penetra diretamente
            na pele. Só o contrai quem anda descalço na terra contaminada por
            fezes humanas. Se não se tratar, a pessoa fica fraca, sem ânimo e
            com a pele amarelada. Daí a doença ser também conhecida como
            amarelão."*

        O parágrafo do exemplo possui 5 sentenças.
    """

    name = 'Mean sentences per paragraph'
    column_name = 'sentences_per_paragraph'

    def value_for_text(self, t, rp=default_rp):
        return Sentences().value_for_text(t) / Paragraphs().value_for_text(t)


class SyllablesPerContentWord(base.Metric):
    """
        ## Sílabas por Palavra de Conteúdo:

        Número médio de sílabas por palavras de conteúdo (substantivos, verbos,
        adjetivos e advérbios).

        ### Exemplo:

        *"Acessório utilizado por adolescentes, o boné é um dos itens que
            compõem a vestimenta idealizada pela proposta."*

        Número de sílabas por palavras de conteúdo do exemplo é 3,5.
    """

    name = 'Mean syllables per content word'
    column_name = 'syllables_per_content_word'

    def value_for_text(self, t, rp=default_rp):
        content_tokens = filter(pos_tagger.tagset.is_content_word,
                                rp.tagged_words(t))
        content_words = map(lambda t: t[0], content_tokens)

        syllables = map(syllable_separator.separate, content_words)

        nwords = 0
        nsyllables = 0
        for w in syllables:
            nwords += 1
            nsyllables += len(w)

        return nsyllables / nwords


class VerbIncidence(base.Metric):
    """
        ## Incidência de Verbos:

        Incidência de verbos em um texto.

        ### Exemplo:

        *"Acessório utilizado por adolescentes, o boné é um dos itens que
            compõem a vestimenta idealizada pela proposta."*

        Com 4 verbos e 17 palavras, a incidência de verbos é 235,29 (número
            de verbos/(número de palavras /1000)).
    """

    name = 'Verb incidence'
    column_name = 'verbs'

    def value_for_text(self, t, rp=default_rp):
        verbs = [t for t in rp.tagged_words(t)
                 if pos_tagger.tagset.is_verb(t)
                 or pos_tagger.tagset.is_auxiliary_verb(t)
                 or pos_tagger.tagset.is_participle(t)]
        return len(verbs) / (len(rp.all_words(t)) / 1000)


class NounIncidence(base.Metric):
    """
        ## Incidência de Substantivos:

        Incidência de substantivos em um texto.

        ### Exemplo:

        *"Acessório utilizado por adolescentes, o boné é um dos itens que
            compõem a vestimenta idealizada pela proposta."*

        Com 6 substantivos e 17 palavras, a incidência de substantivos é
            352,94 (número de substantivos/(número de palavras /1000)).
    """

    name = 'Noun incidence'
    column_name = 'nouns'

    def value_for_text(self, t, rp=default_rp):
        nouns = filter(pos_tagger.tagset.is_noun, rp.tagged_words(t))
        return ilen(nouns) / (ilen(rp.all_words(t)) / 1000)


class AdjectiveIncidence(base.Metric):
    """
        ## Incidência de Adjetivos:

        Incidência de adjetivos em um texto.

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

        Com 6 adjetivos e 95 palavras, a incidência de adjetivos é 63,157
        (número de adjetivos/(número de palavras/1000)).
    """

    name = 'Adjective incidence'
    column_name = 'adjectives'

    def value_for_text(self, t, rp=default_rp):
        adjectives = filter(pos_tagger.tagset.is_adjective, rp.tagged_words(t))
        return ilen(adjectives) / (ilen(rp.all_words(t)) / 1000)


class AdverbIncidence(base.Metric):
    """
        ## Incidência de Advérbios:

        Incidência de advérbios em um texto.

        ### Exemplo:

        *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
            Já não temos recursos suficientes para a manutenção das escolas,
            por exemplo, e também precisamos valorizar o magistério - justifica
            a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*

        Com 8 advérbios e 38 palavras, a incidência de adjetivos é 210,526
            (número de advérbios/(número de palavras/1000)).
    """

    name = 'Adverb incidence'
    column_name = 'adverbs'

    def value_for_text(self, t, rp=default_rp):
        adverbs = [t for t in rp.tagged_words(t)
                   if pos_tagger.tagset.is_adverb(t)
                   or pos_tagger.tagset.is_denotative_word(t)]
        return ilen(adverbs) / (ilen(rp.all_words(t)) / 1000)


class PronounIncidence(base.Metric):
    """
        ## Incidência de Pronomes:

        Incidência de pronomes em um texto.

        ### Exemplo:

        *"Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça
            entre os itens do uniforme de alunos dos ensinos Fundamental e
            Médio nas escolas municipais, estaduais e federais. Ele defende a
            medida como forma de proteger crianças e adolescentes dos males
            provocados pelo excesso de exposição aos raios solares. Se a idéia
            for aprovada, os estudantes receberão dois conjuntos anuais,
            completados por calçado, meias, calça e camiseta."*

        Com 2 pronomes e 69 palavras, a incidência de pronomes é 28,98
            (número de pronomes/(número de palavras/1000)).
    """

    name = 'Pronoun incidence'
    column_name = 'pronouns'

    def value_for_text(self, t, rp=default_rp):
        pronouns = filter(pos_tagger.tagset.is_pronoun, rp.tagged_words(t))
        return ilen(pronouns) / (ilen(rp.all_words(t)) / 1000)


class ContentWordIncidence(base.Metric):
    """
        ## Incidência de Palavras de Conteúdo:

        Incidência de palavras de conteúdo em um texto. Palavras de conteúdo
        são substantivos, verbos, adjetivos e advérbios.

        ### Exemplo:

        *"Não podemos acrescentar nenhuma despesa a mais no nosso orçamento.
            Já não temos recursos suficientes para a manutenção das escolas,
            por exemplo, e também precisamos valorizar o magistério - justifica
            a diretora do Departamento Pedagógico da SEC, Sonia Balzano."*

        Com 27 palavras de conteúdo e 38 palavras, a incidência de palavras
            de conteúdo é 710,526 (número de palavras de conteúdo/(número de
            palavras/1000)).
    """

    name = 'Content word incidence'
    column_name = 'content_words'

    def value_for_text(self, t, rp=default_rp):
        content_words = filter(pos_tagger.tagset.is_content_word,
                               rp.tagged_words(t))
        return ilen(content_words) / (ilen(rp.all_words(t)) / 1000)


class FunctionWordIncidence(base.Metric):
    """
        ## Incidência de Palavras Funcionais:

        Incidência de palavras funcionais em um texto. Palavras funcionais são
        artigos, preposições, pronomes, conjunções e interjeições.

        ### Exemplo:

        *"Foi o senador Flávio Arns (PT-PR) quem sugeriu a inclusão da peça
            entre os itens do uniforme de alunos dos ensinos Fundamental e
            Médio nas escolas municipais, estaduais e federais. Ele defende a
            medida como forma de proteger crianças e adolescentes dos males
            provocados pelo excesso de exposição aos raios solares. Se a idéia
            for aprovada, os estudantes receberão dois conjuntos anuais,
            completados por calçado, meias, calça e camiseta."*

        Com 26 palavras funcionais e 69 palavras, a incidência de palavras
            funcionais é 376,81 (número de palavras funcionais/(número de
            palavras/1000)).
    """

    name = 'Function word incidence'
    column_name = 'function_words'

    def value_for_text(self, t, rp=default_rp):
        function_words = filter(pos_tagger.tagset.is_function_word,
                                rp.tagged_words(t))
        return ilen(function_words) / (ilen(rp.all_words(t)) / 1000)


class BasicCounts(base.Category):
    name = 'Basic Counts'
    table_name = 'basic_counts'

    def __init__(self):
        super(BasicCounts, self).__init__()
        self._set_metrics_from_module(__name__)
        self.metrics.sort(key=lambda m: m.name)

    def values_for_text(self, t, rp=default_rp):
        return super(BasicCounts, self).values_for_text(t, rp)
