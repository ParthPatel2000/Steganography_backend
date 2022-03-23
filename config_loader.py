import yaml

# write a function to transfer config from c# raw_data.yaml to this config.


def read(query):
    with open("config.yaml") as config_file:
        data = yaml.safe_load(config_file)
    return eval(query)


