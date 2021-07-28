import json


def load_config(filename: str) -> dict:
    with open(filename) as json_file:
        data = json.load(json_file)

    return data
