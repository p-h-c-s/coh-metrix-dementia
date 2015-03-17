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
from math import log
import numpy as np
from scipy import dot
from scipy.linalg import inv, svd, diagsvd, norm


class LSASpace(object):
    """Represents an LSA space, that can be used to compute similarities
    between text fragments (texts, paragraphs, sentences, and so on).
    """

    def __init__(self, docs, k):
        self.terms = self.get_terms(iter(docs))
        self.txd = self.build_txd_matrix(self.terms, docs)
        self.apply_tf_idf(self.txd)
        self.sk_Uk = self.apply_lsa(self.txd, k)

    @staticmethod
    def get_terms(documents):
        """Return an alfabetical list of the unique words present in a
        collection of documents.

        :documents: an interator that returns lists of strings.
        """
        terms = set()

        for doc in documents:
            for word in doc:
                terms.add(word)

        return sorted(list(terms))

    @staticmethod
    def build_txd_matrix(terms, documents, ndocuments=1):
        """Build a term-by-document (TxD) matrix.

        :terms: a list of the unique terms present in the document collection.
        :documents: an interator that returns lists of strings.
        :ndocuments: the approximate number of documents expected to be
            returned by the iterator.

        :returns: a len(terms) x ndocuments np.ndarray object, representing
            the TxD matrix.
        """
        if isinstance(documents, list) or isinstance(documents, tuple):
            ndocuments = len(documents)

        txd = np.zeros((len(terms), ndocuments), dtype=np.float64)

        for j, doc in enumerate(iter(documents)):
            for i, term in enumerate(terms):
                txd[i, j] = doc.count(term)

        return txd

    @staticmethod
    def apply_tf_idf(txd):
        """Apply (IN PLACE) a term frequency * inverse document frequency
        transformation to a TxD matrix. The transformation uses:

            tf(t,d) = 1 + log f(t,d) if f(t, d) is not zero, and zero otherwise.
            idf = log(N / (1 + n_t))

        :txd: the TxD matrix.
        """
        rows, cols = txd.shape

        doc_freqs = np.zeros(rows, dtype=np.float64)

        for t in range(rows):
            for d in range(cols):
                if txd[t, d] != 0.0:
                    doc_freqs[t] += 1.0

        print('doc_freqs', doc_freqs, rows, cols)

        for t in range(rows):
            for d in range(cols):
                tf = (1.0 + log(txd[t, d])) if txd[t, d] != 0.0 else 0.0
                idf = log(cols / (1.0 + doc_freqs[t]))

                txd[t, d] = tf * idf

    @staticmethod
    def apply_lsa(txd, k):
        """Use SVD to decompose a TxD matrix C, and find C_k, its lower rank
        approximation.

        :txd: a TxD matrix.
        :k: the number of eigenvalues to keep.

        :return: the product sigma_k^-1 * U_k^T, which can be used to map query
        vectors into the vector space.
        """
        U, s, Vh = svd(txd, full_matrices=False, check_finite=False)

        for i in range(k, len(s)):
            s[i] = 0

        sk_Uk = dot(inv(diagsvd(s[:k], k, k)), U[:, :k].transpose())

        return sk_Uk

    def build_query_vector(self, query):
        """Calculate the frequence of ocurrence in the query of each term
        belonging to the LSA space, and multiplies the corresponding vector by
        the sigma_k^-1 * U_k^T matrix, to map it into the LSA space.

        :query: a list of strings.
        """
        q = np.zeros(len(self.terms))

        for i, term in enumerate(self.terms):
            q[i] = query.count(term)

        return dot(self.sk_Uk, q)

    def compute_similarity(self, q1, q2):
        """Calculate the cosine similarity of two queries.

        :q1: a list of strings.
        :q2: another list of strings.
        :returns: a number between 0 and 1, measuring the similarity between q1
        and q2.
        """
        q1k = self.build_query_vector(q1)
        q2k = self.build_query_vector(q2)

        return dot(q1k, q2k) / (norm(q1k) * norm(q2k))

if __name__ == '__main__':
    docs = [['o', 'livro', 'está', 'sobre', 'a', 'mesa'],
            ['o', 'livro', 'é', 'meu'],
            ['o', 'livro', 'é', 'da', 'mesa']]

    space = LSASpace(docs, k=2)

    print(', '.join(space.terms))
    print(space.txd)

    print(space.build_query_vector(
        ['o', 'livro', 'está', 'sobre', 'o', 'livro']))

    print(space.compute_similarity(
        ['o', 'livro', 'está', 'sobre', 'o', 'livro'],
        ['a', 'mesa']))
    print(space.compute_similarity(
        ['o', 'livro', 'está', 'sobre', 'o', 'livro'],
        ['o', 'livro', 'está', 'sobre', 'a', 'mesa'],))
    print(space.compute_similarity(
        ['o', 'livro', 'está', 'sobre', 'o', 'livro'],
        ['o', 'livro', 'está', 'sobre', 'o', 'livro'],))
