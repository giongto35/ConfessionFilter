import os

# Base directory
__base_dir__ = os.path.dirname(__file__)

# Training directory
training_directory = os.path.join(__base_dir__, '../Data', 'training')

# Testing directory
testing_directory = os.path.join(__base_dir__, '../Data', 'testing')

# Raw documents
raw_document_folder = 'raw'

# Positive documents
pos_document_folder = 'pos'

# Negative documents
neg_document_folder = 'neg'
