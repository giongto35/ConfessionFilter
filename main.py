#!/usr/bin/env python
import os
import sys

from utils import *
from formalize import formalize_all_files
from parse import parse_all_terms
from tfidf_weighting import TFIDFWeighting
from query_dot import classify


if __name__ == '__main__':
    # Formalize dataset
    formalize_all_files('training_data')

    # Load all data
    dictionary = {}
    pos_files = get_all_files('training_data/pos')
    pos_docs = []
    for file in pos_files:
        pos_docs.extend(parse_all_terms(dictionary, 'training_data/pos/' + file))

    neg_files = get_all_files('training_data/neg')
    neg_docs = []
    for file in neg_files:
        neg_docs.extend(parse_all_terms(dictionary, 'training_data/neg/' + file))

    # Build inverted index
    n_terms = len(dictionary)
    inverted_index = TFIDFWeighting(n_terms)

    category = []
    for doc in pos_docs:
        inverted_index.add(dictionary, len(category), doc)
        category.append(1)

    for doc in neg_docs:
        inverted_index.add(dictionary, len(category), doc)
        category.append(-1)

    # Build tfidf based on inverted index
    inverted_index.build_tfidf(len(category))

    # Formalize query
    formalize_all_files('testing_data')

    # Loading all query
    pos_files = get_all_files('testing_data/pos')
    pos_docs = []
    for file in pos_files:
        pos_docs.extend(parse_all_terms(dictionary, 'testing_data/pos/' + file))

    neg_files = get_all_files('testing_data/neg')
    neg_docs = []
    for file in neg_files:
        neg_docs.extend(parse_all_terms(dictionary, 'testing_data/neg/' + file))

    n_query = len(pos_docs) + len(neg_docs)
    n_correct = 0

    for doc in pos_docs:
        query = inverted_index.make_query_tfidf(dictionary, doc)
        result = classify(inverted_index=inverted_index, category=category, query=query)

        if result == 'OK':
            n_correct = n_correct + 1

    for doc in neg_docs:
        query = inverted_index.make_query_tfidf(dictionary, doc)
        result = classify(inverted_index=inverted_index, category=category, query=query)

        if result == 'ERR':
            n_correct = n_correct + 1

    print 'Precision = %f' % (float(n_correct) / n_query)
