import os
import yaml
class config(object):
    def __init__(self,config_path):
        with open(config_path) as config_file:
            yaml_config = yaml.safe_load(config_file)
        self.config = yaml_config
        self.parse_values()
    def parse_values(self):
        for component in self.config:
            for config_param in self.config[component]:
                self.config[component][config_param] = os.getenv(component.upper()+"_"+component.upper(),self.config[component][config_param])
    def get_component(self,component):
        return self.config.get(component,{})