import math

from inverted_index import InvertedIndex


class CagegoryIndex(InvertedIndex):

    def __init__(self, n_terms):
        InvertedIndex.__init__(self, n_terms)

    def build(self, category):
        n_terms = len(self.index)

        self.frequency = [None] * 2
        self.frequency[0] = [0] * n_terms
        self.frequency[1] = [0] * n_terms

        self.sum_frequency = [0] * 2

        for i in range(len(self.index)):
            for j in range(len(self.index[i])):
                self.frequency[category[self.index[i][j]]][i] += self.freq[i][j]
                self.sum_frequency[category[self.index[i][j]]] += self.freq[i][j]

    def classify(self, dictionary, doc, verbose=False):
        n_terms = len(self.index)

        ret = None
        ret_score = 0

        for category in range(2):
            score = math.log(float(self.sum_frequency[category]) / n_terms)
            for field in doc:
                term = field['term']
                weight = field['weight']
                freq = 0
                if term in dictionary:
                    freq = self.frequency[category][dictionary[term]]
                score += math.log(weight * (freq + 1.0) / (self.sum_frequency[category] + n_terms))

            if ret is None or ret_score < score:
                ret = category
                ret_score = score

        if verbose and ret == 1:
            print 'Score %f' % ret_score

        return ret
