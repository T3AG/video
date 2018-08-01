from os.path import isfile, join
from os import listdir
import pickle

'''
cd /media/alan/343EFB573EFB111A/Box\ Sync/git/video/data
'''

# Path directories
paths = {
    'data_path'     : '../../s3/FF-Data/',
    'ibm_path'      : '!data/benchmark_ibm_',
    'google_path'   : '!data/benchmark_google_'
}


# Helper functions
# Inputs input paths, returns all file paths at directory
def get_paths(input_paths):
    return [f for f in listdir(input_paths) if isfile(join(input_paths, f))]


# Inputs output file path and data, saves as pickle
def save_to_pickle(output_dir, output_data):
    pickle.dump(output_data, open(output_dir, "wb"))
