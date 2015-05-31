import os
import json
import re
import sys

import numpy as np

from utils import get_all_files
from configurations import dictionary_directory


# Apply overflow hashing algorithm to reduce the size of term stored in memory
def hash(term, base=np.int32(1000033)):
    ret = np.int32(0)
    for i in range(len(term)):
        ret = ret * base + ord(term[i])
    return int(ret)


# Group's weight = 1 / (2 ^ group_size)
def extract_all_terms(dictionary, path, fixed_dictionary=False, use_external_dictionaries=False, max_group_terms_size=4):

    np.warnings.simplefilter("ignore", RuntimeWarning)
    all_docs = []

    if use_external_dictionaries:

        # Check if the dictionary is empty or not
        if len(dictionary) == 0:
            # Load external dictionaries
            dict_files = get_all_files(dictionary_directory)
            for dict_file in dict_files:
                terms = open(os.path.join(dictionary_directory, dict_file), 'r').readlines()
                for term in terms:
                    term = term.lower().strip()
                    hash_term = hash(term)
                    if hash_term not in dictionary:
                        dictionary[hash_term] = len(dictionary)

        with open(path, 'r') as file:
            docs = json.load(file)
            for doc in docs:

                # Split terms
                terms = []
                term = ''
                for i in range(len(doc)):
                    if doc[i].isdigit() is False and doc[i].isalpha() is False:
                        if len(term) > 0:
                            terms.append(term.lower())
                        term = ''
                    else:
                        term += doc[i]
                if len(term) > 0:
                    terms.append(term.lower())

                # terms = re.split(r'[ ,;:()]+', doc)

                extracted_doc = []
                for i in range(len(terms)):
                    j = 0
                    term = ''
                    weight = 1
                    while j < max_group_terms_size and i + j < len(terms):
                        if len(term) > 0:
                            term += ' '
                        term += terms[i]
                        hash_term = hash(term)
                        if hash_term in dictionary:
                            extracted_doc.append({'term': hash_term, 'weight': weight})

                        weight /= 2.0
                        j += 1

                all_docs.append(extracted_doc)

    else:
        print path
        with open(path, 'r') as file:
            docs = json.load(file)

            for doc in docs:
                # Split terms
                terms = []
                term = ''
                for i in range(len(doc)):
                    if doc[i].isdigit() is False and doc[i].isalpha() is False:
                        if len(term) > 0:
                            terms.append(term.lower())
                        term = ''
                    else:
                        term += doc[i]
                if len(term) > 0:
                    terms.append(term.lower())

                extracted_doc = []
                for i in range(len(terms)):
                    j = 0
                    term = ''
                    weight = 1
                    while j < max_group_terms_size and i + j < len(terms):
                        if len(term) > 0:
                            term += ' '
                        term += terms[i]
                        hash_term = hash(term)
                        if len(term) > 0 and hash_term not in dictionary:
                            if not fixed_dictionary:
                                dictionary[hash_term] = len(dictionary)
                        if len(term) > 0 and hash_term in dictionary:
                            extracted_doc.append({'term': hash_term, 'weight': weight})

                        weight /= 2.0
                        j += 1

                all_docs.append(extracted_doc)

    return all_docs
