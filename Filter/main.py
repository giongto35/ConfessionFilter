#!/usr/bin/env python

import os
import sys

from utils import *
from configurations import *
from formalize import formalize_all_files
from extractor import extract_all_terms

from inverted_index import InvertedIndex
from tfidf_weighting import TFIDFWeighting
from category_index import CagegoryIndex


if __name__ == '__main__':

    training_positive_directory = os.path.join(training_directory, pos_document_folder)
    training_negative_directory = os.path.join(training_directory, neg_document_folder)

    testing_positive_directory = os.path.join(testing_directory, pos_document_folder)
    testing_negative_directory = os.path.join(testing_directory, neg_document_folder)

    dictionary = {}
    category = []
    inverted_index = InvertedIndex(0)

    # Initialize data for classify
    def intialize():
        # Use global variables
        global dictionary
        global category
        global inverted_index

        # Formalization
        formalize_all_files(training_directory)
        formalize_all_files(testing_directory)

        # Load all data
        pos_files = get_all_files(training_positive_directory)
        pos_docs = []
        for file in pos_files:
            if "json" in file:
                pos_docs.extend(extract_all_terms(dictionary, os.path.join(training_positive_directory, file), use_external_dictionaries=False))

        neg_files = get_all_files(training_negative_directory)
        neg_docs = []
        for file in neg_files:
            if "json" in file:
                neg_docs.extend(extract_all_terms(dictionary, os.path.join(training_negative_directory, file), use_external_dictionaries=False))

        # Choose the right algorithm
        if sys.argv[1] == 'dot':

            # Build inverted index
            n_terms = len(dictionary)
            inverted_index = TFIDFWeighting(n_terms)

            for doc in pos_docs:
                inverted_index.add(dictionary, len(category), doc)
                category.append(1)

            for doc in neg_docs:
                inverted_index.add(dictionary, len(category), doc)
                category.append(0)

            # Build tfidf based on inverted index
            inverted_index.build(len(category))

        elif sys.argv[1] == 'bayes':

            # Build inverted index
            n_terms = len(dictionary)
            inverted_index = CagegoryIndex(n_terms)

            for doc in pos_docs:
                inverted_index.add(dictionary, len(category), doc)
                category.append(1)

            for doc in neg_docs:
                inverted_index.add(dictionary, len(category), doc)
                category.append(0)

            # Initialize for bayes
            inverted_index.build(category)

    # Evaluate the result
    # Compute ratio between false_positive and (false_negative + false_positive)
    def evaluate():
        # Use global variables
        global dictionary
        global category
        global inverted_index

        # Loading all query
        pos_files = get_all_files(testing_positive_directory)
        pos_docs = []
        for file in pos_files:
            if "json" in file:
                pos_docs.extend(extract_all_terms(dictionary, os.path.join(testing_positive_directory, file), fixed_dictionary=True, use_external_dictionaries=False))

        neg_files = get_all_files(testing_negative_directory)
        neg_docs = []
        for file in neg_files:
            if "json" in file:
                neg_docs.extend(extract_all_terms(dictionary, os.path.join(testing_negative_directory, file), fixed_dictionary=True, use_external_dictionaries=False))

        false_negative = 0
        false_positive = 0

        for i in range(len(pos_docs)):
            # Choose the right algorithm
            if sys.argv[1] == 'dot':
                result = inverted_index.classify(dictionary=dictionary, category=category, doc=pos_docs[i])
            elif sys.argv[1] == 'bayes':
                result = inverted_index.classify(dictionary=dictionary, doc=pos_docs[i])

            # n_query += 1
            # if result == 1:
            #     n_correct += 1
            if result == 0:
                false_positive += 1

                print '#%d Expected=1, Given=%d, Ratio=%f' % (i, result, false_positive / float(false_positive + false_negative))

        for i in range(len(neg_docs)):
            # Choose the right algorithm
            if sys.argv[1] == 'dot':
                result = inverted_index.classify(dictionary=dictionary, category=category, doc=neg_docs[i])
            elif sys.argv[1] == 'bayes':
                result = inverted_index.classify(dictionary=dictionary, doc=neg_docs[i])

            # n_query += 1
            # if result == 0:
            #     n_correct += 1
            # else:
            #     document = ""
            #     for term in neg_docs[i]:
            #         document = document + ' ' + term
            #     print document
            if result == 0:
                false_negative += 1

                print '#%d Expected=0, Given=%d, Ratio=%f' % (i, result, false_positive / float(false_positive + false_negative))

    intialize()
    evaluate()
