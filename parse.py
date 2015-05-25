import json
import re


def parse_all_terms(dictionary, path):
    all_docs = []
    with open(path, 'r') as file:
        docs = json.load(file)
        for doc in docs:
            terms = re.split(r'[ ,;:()]+', doc)
            for term in terms:
                if len(term) > 0 and term not in dictionary:
                    dictionary[term] = len(dictionary)
            all_docs.append(terms)
    return all_docs
