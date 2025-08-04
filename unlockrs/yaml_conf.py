import yaml
import os

async def load_yaml_file(dir_path="nd"):
    config_file = "config.yml"
    allitems = os.listdir(dir_path)
    if config_file in allitems:
        file_path = os.path.join(dir_path, config_file)
    with open(file_path) as file:
        try:
            data = yaml.safe_load(file)
            print(f"Yaml Files has been loaded from {file_path}")
            return data
        except yaml.YAMLError as e:
            print(f"Error loading YAML file: {e}")
            return
        
async def setup_configfile(dir_path):
    load = await load_yaml_file(dir_path=dir_path)
# Import the TrueNas Global Variables
    return load