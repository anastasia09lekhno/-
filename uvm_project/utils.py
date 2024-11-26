import yaml

def save_yaml(data, file_path):
    with open(file_path, "w") as f:
        yaml.dump(data, f)

