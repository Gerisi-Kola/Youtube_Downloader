import json

def get_json(file_name):
    file = open(file_name,"r")
    data = json.load(file)
    file.close()
    return data

def save_json(file_name,data):
    file = open(file_name,"w")
    json.dump(data,file, indent = 6)
    file.close()

def save_bin(file_name):
    file = open(file_name,"wb")
    file.write()
    file.close()


if __name__ == "__main__":
    """a = get_json("settings.json")
    print(a)"""
    b = {
        "a":1,
        "b":2,
        "c":3
    }
    save_json("./working_progress/file.log",b)
