from os import listdir
from os.path import isfile, join
import json


def is_json(file):
    """Check if a file is json

    Arguments:
        file {string} -- Path to the file

    Returns:
        Boolean -- Whether it's a json file or not
    """
    if isfile(file) and file.endswith('.json'):
        return True
    else:
        return False


def get_websites_info_files(dir):
    """Get the path for all json files inside a directory

    Arguments:
        dir {String} -- path to the directory

    Returns:
        List -- all paths for the json files
    """
    files = [join(dir, f) for f in listdir(dir) if is_json(join(dir, f))]
    return files


def load_data(files):
    """Load the json as a dict for each file and returns a dict containing each file dict

    Arguments:
        files {List} -- path for the json files

    Returns:
        List -- list containing all the data
    """
    data = []

    for file_ in files:
        loaded_file = json.load(open(file_))
        data.append(loaded_file)

    return data

def load(dir):
    """Load everything

    Arguments:
        dir {String} -- path to the directory containing the json files

    Returns:
        List -- list that contains all the data
    """
    files = get_websites_info_files(dir)
    data = load_data(files)
    return data