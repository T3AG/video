from os import listdir
from os.path import isfile, join
from shutil import copyfile
import pickle


path = '../Video_Classification/!data/'
beg_string_ibm = 'benchmark_ibm_'
beg_string_google = 'benchmark_google_'
pick = '.pickle'

# Inputs input paths, returns all file paths at directory
def get_paths(input_paths):
    return [f for f in listdir(input_paths) if isfile(join(input_paths, f))]


def process_ibm(json):
    results = json['results']
    for transcript in results:
        print(transcript['alternatives'][0]['transcript'])

    return


files = get_paths(path)
for file in files:
    if pick in file:
        if beg_string_ibm in file:
            print()
            print(file)
            print()
            string = pickle.load(open(path+file, "rb"))
            process_ibm(string)
        elif beg_string_google in file:
            pass
