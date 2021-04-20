import yaml
import os

class MysqlConfig:
    mysql_conf_file = ""
    def __init__(self):
        TAG = "mysql_config:"
        my_dir = os.getcwd()
        print(TAG, "current dir=", my_dir)
        self.mysql_conf_file = my_dir + "/database_config.yaml"
    def showData(self):
        print("Testing")
    def callDBConfig(self):
        TAG = "callDBConfig"
        with open(self.mysql_conf_file) as my_config:
            # print(TAG, yaml.load(my_config, Loader=yaml.FullLoader))
            # return yaml.load(my_config, Loader=yaml.FullLoader)
            return yaml.safe_load(my_config)