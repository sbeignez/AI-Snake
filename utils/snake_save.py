import json

def save(data, file_name = "data.json", overwrite=True):

    with open(file_name, 'w') as f:
        json.dump(data, f)


def load(file_name = "data.json"):

    with open(file_name, 'r') as f:
        file = json.load(f)
    return file


if __name__ == '__main__':
    pass

    config = {"key1": "value1", "key2": "value2"}
    save(config, file_name="data/new.json")

    o = load(file_name="data/new.json")
    print(o, type(o))