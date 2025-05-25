import os
import datetime
from json_controler import get_json,save_json

def today_log_get():
    x = datetime.datetime.now()
    
    log_file = x.strftime("%x").replace("/","-")
    log_file += ".log"
    print(log_file)
    
    if os.path.exists("./history/"+log_file):
        return get_json(log_file), log_file
    else:
        print("file doesn't exist")
        return {}, log_file


def save_log_converter(log):
    pass
    

if __name__ == "__main__":
    today_log_get()