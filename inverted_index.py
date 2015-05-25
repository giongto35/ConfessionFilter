class InvertedIndex(object):
    index = []
    freq = []

    def __init__(self, n_terms):
        super(InvertedIndex, self).__init__()
        self.index = [[]] * n_terms
        self.freq = [[]] * n_terms

    def add(self, dictionary, doc_id, doc_content):
        for term in doc_content:
            if term in dictionary:
                term_id = dictionary[term]
                if len(self.index[term_id]) == 0 or self.index[term_id][-1] != doc_id:
                    self.index[term_id].append(doc_id)
                    self.freq[term_id].append(0)
                self.freq[term_id][-1] = self.freq[term_id][-1] + 1
