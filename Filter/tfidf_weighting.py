import math

from inverted_index import InvertedIndex


class TFIDFWeighting(InvertedIndex):

    def __init__(self, n_terms):
        InvertedIndex.__init__(self, n_terms)

    def build(self, n_docs):
        self.n_docs = n_docs
        n_terms = len(self.index)

        self.tfidf = [None] * n_terms

        sum_freq = [0] * n_docs
        for i in range(n_terms):
            for j in range(len(self.index[i])):
                sum_freq[self.index[i][j]] += self.freq[i][j]

        for i in range(n_terms):
            idf = math.log(float(n_docs) / len(self.index[i]))
            self.tfidf[i] = []
            for j in range(len(self.index[i])):
                tf = float(self.freq[i][j]) / sum_freq[self.index[i][j]]

                self.tfidf[i].append(tf * idf)

    def make_query_tfidf(self, dictionary, query):
        n_terms = len(self.index)

        sum_freq = 0
        freq = [0] * n_terms
        for field in query:
            term = field['term']
            weight = field['weight']
            if term in dictionary:
                freq[dictionary[term]] += weight
                sum_freq += weight

        tfidf = [0] * n_terms
        for i in range(n_terms):
            idf = math.log(float(self.n_docs) / len(self.index[i]))
            tf = float(freq[i]) / sum_freq

            tfidf[i] = tf * idf

        return tfidf

    def classify(self, dictionary, category, doc, top_k=50, ratio_threshold=0.60, similarity_threshold=0.0003, verbose=False):
        query = self.make_query_tfidf(dictionary, doc)

        n_terms = len(query)

        n_docs = self.n_docs
        similarity = [0] * n_docs

        for i in range(n_terms):
            if query[i] > 0:
                for j in range(len(self.index[i])):
                    id = self.index[i][j]
                    similarity[id] = similarity[id] + query[i] * self.tfidf[i][j]

        ranked_list = sorted(range(n_docs), key=lambda k: -similarity[k])
        top_k = min(top_k, n_docs)

        n_correct = 0
        for i in range(min(top_k, n_docs)):
            id = ranked_list[i]
            if similarity[id] == 0:  # or similarity[id] < similarity[ranked_list[0]] / 2:
                top_k = i
                break
            if category[id] == 1:
                n_correct += 1

        if top_k == 0:
            return 0

        if verbose:
            print '%d / %d - %f, %f' % (n_correct, top_k, similarity[ranked_list[0]], similarity[ranked_list[top_k - 1]])

        if float(n_correct) / top_k > ratio_threshold:
            return 1
        else:
            return 0
