import json
import re


def extract_all_terms(dictionary, path, fixed_dictionary=False):
    all_docs = []
    with open(path, 'r') as file:
        docs = json.load(file)
        for doc in docs:
            terms = re.split(r'[ ,;:()]+', doc)
            doc = []
            for i in range(len(terms)):
                if len(terms[i]) > 0 and terms[i] not in dictionary:
                    if fixed_dictionary:
                        continue
                    dictionary[terms[i]] = len(dictionary)
                if len(terms[i]) > 0:
                    doc.append({"term": terms[i], "weight": 1})
            all_docs.append(doc)
    return all_docs
