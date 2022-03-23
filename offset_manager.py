import yaml

def read(query):
    with open("offset.yaml") as offset_file:
        data = yaml.safe_load(offset_file)
    return eval(query)