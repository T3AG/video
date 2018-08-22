from functions import get_paths, save_to_pickle, save_to_txt
import subprocess
import requests
import pickle
import json
import os


# Inputs json, parses relavent portions and returns as string
def parse_to_txt(json):
    return ''.join([text['alternatives'][0]['transcript'] for text in json['results']])


# Inputs file path and audio path, outputs audio to audio path
def extract_audio(file, audio):
    FNULL = open(os.devnull, 'w')
    subprocess.call(['ffmpeg', '-i', file, '-codec:a', 'pcm_s16le', '-ac', '1', audio], stdout=FNULL, stderr=subprocess.STDOUT)
    return


# Inputs path to credentials, and access type, outputs parsed credentials
def get_cred(string, path):
    with open(path) as f:
        parsed = json.load(f)
        select_parsed = parsed[string]

    return select_parsed


# Inputs path and credentials, returns API call response, initialises call parameters, makes call
def post_request(path, cred):

    auth = (cred['username'], cred['password'])

    data = open(path, 'rb').read()
    url = 'https://stream.watsonplatform.net/speech-to-text/api/v1/recognize'
    headers = {
        'Content-Type': 'audio/wav',
    }
    params = {'model': 'en-US_NarrowbandModel', 'speaker_labels': 'true'}

    # Obtain and return response
    # response = requests.post(url, headers=headers, data=data, auth=auth)
    response = requests.post(url, headers=headers, data=data, auth=auth, params=params)

    return response


# Run through all input files, obtain annotations for each
def get_return(no_videos, paths):
    input_paths = paths['data_path']
    output_paths = paths['ibm_path']
    auth_path = paths['auth_path']
    cred = get_cred('ibm', auth_path)

    file_names = get_paths(input_paths)[:no_videos]

    for file_name in file_names:
        print(file_name, ': Processing')

        file_path = input_paths + file_name
        output_audio = output_paths + file_name + '.wav'
        output_path = output_paths + file_name + '.pickle'
        output_path_txt = output_paths + file_name + '.txt'

        # Check if file has audio processed, skip if it has
        if not os.path.isfile(output_audio):
            extract_audio(file_path, output_audio)
            print(file_name, ': Audio conversion successful')
        else:
            print(file_name, ': Audio conversion already exists')

        # Check if audio file has been processed, skip if it has
        if not os.path.isfile(output_path):
            response = post_request(output_audio, cred)
            print(file_name, ': Response received')

            # Check if status was successful
            if response.status_code == 200:
                parsed = json.loads(response.text)
                save_to_pickle(output_path, parsed)
                parsed_txt = parse_to_txt(parsed)
                save_to_txt(output_path_txt, parsed_txt)

                print(file_name, ': Response successful')
            else:
                print(file_name, ': Response unsuccessful')
        else:
            print(file_name, ': Response already exists, moving to next file')
