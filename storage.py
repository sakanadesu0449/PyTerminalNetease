import os
import json

ENV_SEP = os.sep
ENV_LINESEP = os.linesep
DEVICE_NAME = os.name

class Account:

    self.ACC_DATA_PATH = 'user'
    self.acc_dict = {}

    def __init__(self):
        
        self.USER_DATA_FORMAT = {
                'alias': ''
                'data': {
                    'last_method': ''
                    'account': ''
                    'password' : ''
                    }
                }
                
        if os.isdir(self.ACC_DATA_PATH) == False:
            os.mkdir(self.ACC_DATA_PATH)

        with open(f'{self.ACC_DATA_PATH}{ENV_SEP}user_data.json', 'r') as json_f:
            self.acc_dict = json.load(json_f)

    def 





