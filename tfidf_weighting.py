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
        for term in query:
            if term in dictionary:
                freq[dictionary[term]] += 1
                sum_freq += 1

        tfidf = [0] * n_terms
        for i in range(n_terms):
            idf = math.log(float(self.n_docs) / len(self.index[i]))
            tf = float(freq[i]) / sum_freq

            tfidf[i] = tf * idf

        return tfidf

    def classify(self, dictionary, category, query, top_k=50, ratio_threshold=0.60, distance_threshold=0.0003):
        query = self.make_query_tfidf(dictionary, query)

        n_terms = len(query)

        n_docs = self.n_docs
        distance = [float('inf')] * n_docs

        for i in range(n_terms):
            if query[i] > 0:
                for j in range(len(self.index[i])):
                    id = self.index[i][j]
                    if distance[id] == float('inf'):
                        distance[id] = 0
                    distance[id] = distance[id] + query[i] * self.tfidf[i][j]

        ranked_list = sorted(range(n_docs), key=lambda k: distance[k])
        top_k = min(top_k, n_docs)

        n_correct = 0
        for i in range(min(top_k, n_docs)):
            id = ranked_list[i]
            if distance[id] == float('inf') or distance[id] > distance[ranked_list[0]] * 2 or distance[id] > distance_threshold:
                top_k = i
                break
            if category[id] == 1:
                n_correct = n_correct + 1

        if top_k == 0:
            return 0

        print '%d / %d - %f, %f' % (n_correct, top_k, distance[ranked_list[0]], distance[ranked_list[top_k - 1]])

        if float(n_correct) / top_k > ratio_threshold:
            return 1
        else:
            return 0
