import yaml
import pathlib

class MysqlConfig:
    mysql_conf_file = ""
    def __init__(self):
        TAG = "mysql_config:"
        print(TAG, "current dir=", pathlib.Path(__file__).resolve().parent)
        self.mysql_conf_file = "./database_config.yaml"
    def showData(self):
        print("Testing")
    def callDBConfig(self):
        TAG = "callDBConfig"
        with open(self.mysql_conf_file) as my_config:
            # print(TAG, yaml.load(my_config, Loader=yaml.FullLoader))
            # return yaml.load(my_config, Loader=yaml.FullLoader)
            return yaml.safe_load(my_config)