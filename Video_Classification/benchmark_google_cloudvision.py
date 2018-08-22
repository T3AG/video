from functions import get_paths, save_to_pickle
from google.cloud import videointelligence
from os.path import isfile, join
from os import listdir
import os.path
import pickle
import os
import io

# Obtain credentials
def get_credentials(auth_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = auth_path


# Inputs video path, outputs video contents
def get_video_contents(path):
    with io.open(path, 'rb') as movie:
        input_content = movie.read()
    return input_content


# Inputs file data, outputs results of annotations
def get_annotations(path_data):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION, videointelligence.enums.Feature.SHOT_CHANGE_DETECTION, ]
    operation = video_client.annotate_video(input_content=path_data, features=features)
    return operation


# Prints all data to console
def print_data(result):
    # Process video/segment level label annotations
    segment_labels = result.annotation_results[0].segment_label_annotations
    for i, segment_label in enumerate(segment_labels):
        print('Video label description: {}'.format(
            segment_label.entity.description))
        for category_entity in segment_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        for i, segment in enumerate(segment_label.segments):
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.nanos / 1e9)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = segment.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
        print('\n')

    # Process shot level label annotations
    shot_labels = result.annotation_results[0].shot_label_annotations
    for i, shot_label in enumerate(shot_labels):
        print('Shot label description: {}'.format(
            shot_label.entity.description))
        for category_entity in shot_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        for i, shot in enumerate(shot_label.segments):
            start_time = (shot.segment.start_time_offset.seconds +
                          shot.segment.start_time_offset.nanos / 1e9)
            end_time = (shot.segment.end_time_offset.seconds +
                        shot.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = shot.confidence
            print('\tSegment {}: {}'.format(i, positions))
            print('\tConfidence: {}'.format(confidence))
        print('\n')

    # Process frame level label annotations
    frame_labels = result.annotation_results[0].frame_label_annotations
    for i, frame_label in enumerate(frame_labels):
        print('Frame label description: {}'.format(
            frame_label.entity.description))
        for category_entity in frame_label.category_entities:
            print('\tLabel category description: {}'.format(
                category_entity.description))

        # Each frame_label_annotation has many frames,
        # here we print information only about the first frame.
        frame = frame_label.frames[0]
        time_offset = (frame.time_offset.seconds +
                       frame.time_offset.nanos / 1e9)
        print('\tFirst frame time offset: {}s'.format(time_offset))
        print('\tFirst frame confidence: {}'.format(frame.confidence))
        print('\n')

    # Process shot changes
    for i, shot in enumerate(result.annotation_results[0].shot_annotations):
        start_time = (shot.start_time_offset.seconds +
                      shot.start_time_offset.nanos / 1e9)
        end_time = (shot.end_time_offset.seconds +
                    shot.end_time_offset.nanos / 1e9)
        print('\tShot {}: {} to {}'.format(i, start_time, end_time))


# Run through all input files, obtain Google annotations for each
def get_return(no_videos, paths):
    input_paths = paths['data_path']
    output_paths = paths['google_path']
    auth_path = paths['google_auth_path']

    get_credentials(auth_path)
    file_names = get_paths(input_paths)[:no_videos]

    for file_name in file_names:
        print(file_name, ': Processing')
        file_path = input_paths + file_name
        output_path = output_paths + file_name + '.pickle'

    # Check if file is already processed, skip if it is
        if not os.path.isfile(output_path):
            content = get_video_contents(file_path)

            operation = get_annotations(content)
            print(file_name, ': Response received')
            result = operation.result()
            print(file_name, ': Response processed successfully')
            save_to_pickle(output_path, result)

            # try:
            #     result = get_annotations(content)
            #     save_to_pickle(output_path, result)
            #     print(file_name, ': Response successful')
            # except:
            #     print(file_name, ': Response unsuccessful')
        else:
            print(file_name, ': Response already exists, moving to next file')



