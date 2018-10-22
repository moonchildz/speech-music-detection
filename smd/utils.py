import os
import numpy as np
import json
import csv
import math
import smd.config as config
import librosa


def read_filelists(folder):
    """Read and return the filelists of a dataset."""
    files = ["mixed_val", "mixed_train", "mixed_test", "noise_train", "music_train", "music_val", "speech_train", "speech_val"]

    dic = {"mixed_val": [],
           "mixed_train": [],
           "mixed_test": [],
           "noise_train": [],
           "music_train": [],
           "music_val": [],
           "speech_train": [],
           "speech_val": []}

    for file in files:
        path = os.path.join(folder, file)
        if os.path.exists(path):
            with open(path, 'r') as f:
                lines = f.readlines()
            for line in lines:
                dic[file].append(line.replace('\n', ''))

    return dic


def read_annotation(filename):
    events = []
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t', quotechar='|')
        for row in spamreader:
            events.append(row)
    return events


def load_audio(filename, duration=None):
    """Load the audio file into a numpy array."""
    return librosa.load(filename, sr=None, duration=duration)[0]


def save_matrix(spec, filename, dst=None):
    """Save a matrix into a .npy file"""
    if dst is None:
        path = filename
    else:
        path = os.path.join(dst, filename)
    np.save(path, spec)


def save_annotation(events, filename, dst=None):
    r"""Save the annotation of an audio file based on the event list.

    The event list has to be formatted this way:

    [
    [t_start, t_end, label],
    [t_start, t_end, label],
    ...
    ]
    """
    if dst is None:
        path = filename
    else:
        path = os.path.join(dst, filename)

    with open(path, "w") as f:
        for event in events:
            f.write(str(event[0]) + '\t' + str(event[1]) + '\t' + event[2] + '\n')


def load_json(filename):
    """Load a json file."""
    with open(filename) as f:
        data = json.load(f)
    return data


def duration_to_frame_count(duration):
    """Return the number of frame for a duration in s."""
    return math.ceil(duration * config.SAMPLING_RATE / config.HOP_LENGTH)