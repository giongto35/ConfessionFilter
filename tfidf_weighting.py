import math

from inverted_index import InvertedIndex


class TFIDFWeighting(InvertedIndex):

    def __init__(self, n_terms):
        InvertedIndex.__init__(self, n_terms)

    def build_tfidf(self, n_docs):
        self.n_docs = n_docs
        n_words = len(self.index)

        print n_words

        self.tfidf = [[]] * n_words
        for i in range(n_words):
            self.tfidf[i] = [None] * len(self.index[i])

        sum_freq = [0] * n_docs
        for i in range(n_words):
            for j in range(len(self.index[i])):
                sum_freq[self.index[i][j]] = sum_freq[self.index[i][j]] + self.freq[i][j]

        for i in range(n_words):
            idf = math.log(float(n_docs) / len(self.index[i]))

            for j in range(len(self.index[i])):
                tf = math.sqrt(float(self.freq[i][j]) / sum_freq[self.index[i][j]])

                self.tfidf[i][j] = tf * idf

    def make_query_tfidf(self, dictionary, query):
        n_words = len(self.index)

        sum_freq = 0
        freq = [0] * n_words
        for term in query:
            if term in dictionary:
                freq[dictionary[term]] = freq[dictionary[term]] + 1
                sum_freq = sum_freq + 1

        tfidf = [0] * n_words
        for i in range(n_words):
            idf = math.log(float(self.n_docs) / len(self.index[i]))
            tf = math.sqrt(float(freq[i]) / sum_freq)

            tfidf[i] = tf * idf

        return tfidf
