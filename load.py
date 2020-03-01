from os import listdir
from os.path import isfile, join
import json


def is_json(file):
    if isfile(file) and file.endswith('.json'):
        return True
    else:
        return False


def get_websites_info_files(dir):
    files = [join(dir, f) for f in listdir(dir) if is_json(join(dir, f))]
    return files


def load_data(files):
    data = []

    for file_ in files:
        loaded_file = json.load(open(file_))
        data.append(loaded_file)

    return data

def load(dir):
    files = get_websites_info_files(dir)
    data = load_data(files)
    return data