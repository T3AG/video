from os.path import isfile, join
from os import listdir
import pickle

# Helper functions
# Inputs input paths, returns all file paths at directory
def get_paths(input_paths):
    return [f for f in listdir(input_paths) if isfile(join(input_paths, f))]


# Inputs output file path and data, saves as pickle
def save_to_pickle(output_dir, output_data):
    pickle.dump(output_data, open(output_dir, "wb"))


# Inputs output file path and data, saves as txt
def save_to_txt(output_dir, output_data):
    with open(output_dir, "w") as file:
        file.write(output_data)


# Completion call back function. Updates global table
def complete():
    print('hi')


# Creates pickle table for all data
def load_table():
    print('hi')


def save_table():
    print('hi')


