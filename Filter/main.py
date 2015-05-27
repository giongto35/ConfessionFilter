#!/usr/bin/env python
import os
import sys

from utils import *
from formalize import formalize_all_files
from parse import parse_all_terms


if __name__ == '__main__':

    # Formalization
    formalize_all_files('training_data')
    formalize_all_files('testing_data')

    # Load all data
    dictionary = {}
    pos_files = get_all_files('training_data/pos')
    pos_docs = []
    for file in pos_files:
        if "json" in file:
            pos_docs.extend(parse_all_terms(dictionary, 'training_data/pos/' + file))

    neg_files = get_all_files('training_data/neg')
    neg_docs = []
    for file in neg_files:
        if "json" in file:
            neg_docs.extend(parse_all_terms(dictionary, 'training_data/neg/' + file))

    if sys.argv[1] == 'dot':

        from tfidf_weighting import TFIDFWeighting

        # Build inverted index
        n_terms = len(dictionary)
        inverted_index = TFIDFWeighting(n_terms)

        category = []
        for doc in pos_docs:
            inverted_index.add(dictionary, len(category), doc)
            category.append(1)

        for doc in neg_docs:
            inverted_index.add(dictionary, len(category), doc)
            category.append(0)

        # Build tfidf based on inverted index
        inverted_index.build(len(category))

        # TESTING PHASE

        # Loading all query
        pos_files = get_all_files('testing_data/pos')
        pos_docs = []
        for file in pos_files:
            if "json" in file:
                pos_docs.extend(parse_all_terms(dictionary, 'testing_data/pos/' + file, fixed_dictionary=True))

        neg_files = get_all_files('testing_data/neg')
        neg_docs = []
        for file in neg_files:
            if "json" in file:
                neg_docs.extend(parse_all_terms(dictionary, 'testing_data/neg/' + file, fixed_dictionary=True))

        n_query = 0
        n_correct = 0

        for i in range(len(pos_docs)):
            result = inverted_index.classify(dictionary=dictionary, category=category, doc=pos_docs[i])

            n_query += 1
            if result == 1:
                n_correct += 1

            print '#%d Expected=1, Given=%s, Precision=%f' % (n_query, result, float(n_correct) / n_query)

        for i in range(len(neg_docs)):
            result = inverted_index.classify(dictionary=dictionary, category=category, doc=neg_docs[i])

            n_query += 1
            if result == 0:
                n_correct += 1
            else:
                document = ""
                for term in neg_docs[i]:
                    document = document + ' ' + term
                print document

            print '#%d Expected=0, Given=%d, Precision=%f' % (n_query, result, float(n_correct) / n_query)

    elif sys.argv[1] == 'bayes':

        from category_index import CagegoryIndex

        # Build inverted index
        n_terms = len(dictionary)
        inverted_index = CagegoryIndex(n_terms)

        category = []
        for doc in pos_docs:
            inverted_index.add(dictionary, len(category), doc)
            category.append(1)

        for doc in neg_docs:
            inverted_index.add(dictionary, len(category), doc)
            category.append(0)

        # Initialize for bayes
        inverted_index.build(category)

        # TESTING PHASE

        # Loading all query
        pos_files = get_all_files('testing_data/pos')
        pos_docs = []
        for file in pos_files:
            if "json" in file:
                pos_docs.extend(parse_all_terms(dictionary, 'testing_data/pos/' + file, fixed_dictionary=True))

        neg_files = get_all_files('testing_data/neg')
        neg_docs = []
        for file in neg_files:
            if "json" in file:
                neg_docs.extend(parse_all_terms(dictionary, 'testing_data/neg/' + file, fixed_dictionary=True))

        n_query = 0
        n_correct = 0

        for i in range(len(pos_docs)):
            result = inverted_index.classify(dictionary=dictionary, doc=pos_docs[i])

            n_query += 1
            if result == 1:
                n_correct += 1

            print '#%d Expected=1, Given=%d, Precision=%f' % (n_query, result, float(n_correct) / n_query)

        for i in range(len(neg_docs)):
            result = inverted_index.classify(dictionary=dictionary, doc=neg_docs[i])

            n_query += 1
            if result == 0:
                n_correct += 1
            else:
                document = ""
                for term in neg_docs[i]:
                    document = document + ' ' + term
                print document

            print '#%d Expected=0, Given=%d, Precision=%f' % (n_query, result, float(n_correct) / n_query)
