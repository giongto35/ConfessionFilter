from os import listdir
from os.path import isfile, join

def get_all_files(path):
    files = []
    for file in listdir(path):
        if isfile(join(path, file)):
            files.append(file)
    return files
