import json

def get_json(file_name: str) -> dict :
    """ Retrieves data from a json file """
    file_name = file_name.replace("\\","/")
    file = open(file_name,"r")
    data = json.load(file)
    file.close()
    return data

def save_json(file_name: str, data: dict) -> None:
    """ Save data in a json file """
    file_name = file_name.replace("\\","/")
    file = open(file_name,"w")
    json.dump(data,file, indent = 4)
    file.close()

def save_bin(file_name: str, data: dict) -> None:
    file_name = file_name.replace("\\","/")
    file = open(file_name,"wb")
    file.write(data)
    file.close()

def save_file(file_name: str, data: dict) -> None:
    """ Save data in a json file """
    file_name = file_name.replace("\\","/")
    file = open(file_name,"w")
    file.write(data)
    file.close()

def read_file(file_name: str) -> str:
    """ Retrieves the content of a file """
    file_name = file_name.replace("\\","/")
    file = open(file_name,"r")
    data = file.read()
    file.close()
    return data

def get_list_of_lines(file_name: str) -> list[str]:
    """ Retrieves the content of a file and split it in all lines """
    file_name = file_name.replace("\\","/")
    file = read_file(file_name)
    file = file.split("\n")
    return file

if __name__ == "__main__":
    """a = get_json("settings.json")
    print(a)"""
    
    """c = read_file(r"D:\Programation\Python\Youtube_Download\history\05-25-25.log")
    print(c)
    c = c.split("\n")
    print(type(c))
    print(c)"""
    
    
    b = {
        "a":1,
        "b":2,
        "c":3
    }
    b = "Hello World"
    save_bin("./working_progress/file.log",b"https://i.ytimg.com/vi_webp/dQw4w9WgXcQ/maxresdefault.webp")
