import csv
import json

from utils import *
from configurations import *


def load_all_data(path, verbose=True):
    if verbose:
        print 'Loading %s' % (path)

    delimiter = ','
    quotechar = '"'

    csvfile = open(path, 'r')
    table = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)

    pos_confs = []
    neg_confs = []

    for row in table:
        # Check whether the confession is positive or negative
        is_positive = False
        for col_id in range(2, len(row)):
            if 'roi' in row[col_id]:
                is_positive = True
                break

        if is_positive:
            pos_confs.append(row[1].decode('utf-8', 'ignore'))
        else:
            neg_confs.append(row[1].decode('utf-8', 'ignore'))

    csvfile.close()

    return pos_confs, neg_confs


def formalize_all_data(path, file, verbose=True):
    if verbose:
        print 'Formalizing %s' % (path)

    pos_confs, neg_confs = load_all_data(path + '/' + raw_document_folder + '/' + file, verbose)

    with open(path + '/' + pos_document_folder + '/' + file.replace('.csv', '.json'), 'w') as pos_file:
        pos_file.write('%s' % json.dumps(pos_confs))

    with open(path + '/' + neg_document_folder + '/' + file.replace('.csv', '.json'), 'w') as neg_file:
        neg_file.write('%s' % json.dumps(neg_confs))


def formalize_all_files(path, verbose=True):
    files = get_all_files(path + '/' + raw_document_folder)
    for file in files:
        formalize_all_data(path=path, file=file, verbose=verbose)
