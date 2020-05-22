import json


def create_file(js):
    with open('currencies.json', 'w+') as write:
        json.dump(js, write, indent=4)


def load_file():
    with open('currencies.json', 'r') as read:
        data = json.load(read)
    return data
