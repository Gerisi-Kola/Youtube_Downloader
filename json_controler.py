import json

#file = "./constant.json"

def get_settings(file):
    data = open(file,"r")
    list_question = json.load(data)
    data.close()
    return list_question




if __name__ == "__main__":
    a = get_settings("settings.json")
    print(a)
