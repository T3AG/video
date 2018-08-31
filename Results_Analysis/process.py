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
    text = ''.join([text['alternatives'][0]['transcript'] for text in json['results']])

    with open('txt.txt', "w") as file:
        file.write(text)
    return text


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
            string = pickle.load(open(path+file, "rb"), encoding='latin1')

            with open(path+file, 'rb') as f:
                print(f)
                u = pickle._Unpickler(f)
                print(u)
                u.encoding = 'latin1'
                p = u.load()
                print(p)
            string = pickle.load(open(path+file, "rb"))

            string = pickle.load(path+file)
            with open(path+file, "rb") as t:
                print(t)
                string = pickle.load(t)
