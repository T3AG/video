from functions import get_paths, save_to_pickle, paths
import subprocess
import requests
import pickle
import json
import os


# Inputs file path and audio path, outputs audio to audio path
def extract_audio(file, audio):
    FNULL = open(os.devnull, 'w')
    subprocess.call(['ffmpeg', '-i', file, '-codec:a', 'pcm_s16le', '-ac', '1', audio], stdout=FNULL, stderr=subprocess.STDOUT)
    return


# Inputs path and credentials, returns API call response, initialises call parameters, makes call
def post_request(path):
    # Watson application credentials
    cred = {
              "url": "https://stream.watsonplatform.net/speech-to-text/api",
              "username": "d0c08233-357a-43e2-bc14-a4b3466a99e7",
              "password": "G8hi5yuEsa7S"
            }

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


# Run through all input files, obtain Google annotations for each
if __name__ == "__main__":

    input_paths = paths['data_path']
    output_paths = paths['ibm_path']

    file_names = get_paths(input_paths)

    for file_name in file_names:
        print(file_name, ': Processing')

        file_path = input_paths + file_name
        output_audio = output_paths + file_name + '.wav'
        output_path = output_paths + file_name + '.pickle'

        # Check if file has audio processed, skip if it has
        if not os.path.isfile(output_audio):
            try:
                extract_audio(file_path, output_audio)
                print(file_name, ': Audio conversion successful')
            except:
                print(file_name, ': Audio conversion unsuccessful')
        else:
            print(file_name, ': Audio conversion already exists')

        # Check if audio file has been processed, skip if it has
        if not os.path.isfile(output_path):
            try:
                response = post_request(output_audio)
                print(file_name, ': Response received')

                # Check if status was successful
                if response.status_code == 200:
                    parsed = json.loads(response.text)
                    save_to_pickle(output_path, parsed)
                    print(file_name, ': Response successful')
                else:
                    print(file_name, ': Response unsuccessful')

            except:
                print(file_name, ': Response not received')
        else:
            print(file_name, ': Response already exists, moving to next file')
