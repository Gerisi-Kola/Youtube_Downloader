import json

#file = "./constant.json"

def get_settings(file_name):
    file = open(file_name,"r")
    data = json.load(data)
    file.close()
    return data

def save_json(file_name,data):
    file = open(file_name,"w")
    file = json.dump(data)
    file.close()

def save_bin(file_name):
    file = open(file_name,"wb")
    file.write()
    file.close()


if __name__ == "__main__":
    a = get_settings("settings.json")
    print(a)
