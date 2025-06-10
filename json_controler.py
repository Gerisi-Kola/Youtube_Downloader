import json
import os

def get_json(file_path: str) -> dict :
    """ Retrieves data from a json file """
    try:
        file_path = file_path.replace("\\","/")
        file = open(file_path,"r")
        data = json.load(file)
        file.close()
        return data
        
    except json.JSONDecodeError:
        print("Erreur : fichier JSON corrompu ou incomplet.")
        return {}

def save_json(file_path: str, data: dict) -> None:
    """ Save data in a json file """
    file_path = file_path.replace("\\","/")
    tmp_path = file_path+".tmp"
    
    with open(tmp_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4,ensure_ascii=False)
        file.flush()               # Vider le buffer Python
        os.fsync(file.fileno())    # Vider le buffer OS (très important)
    
    os.replace(tmp_path, file_path)  # Remplace de façon atomique (sûre)
    """if os.path.exists(tmp_path):
        os.remove(tmp_path)"""

def save_file(file_path: str, data: str) -> None:
    """ Save data in a file """
    file_path = file_path.replace("\\","/")
    tmp_path = file_path+".tmp"
    
    with open(tmp_path, "w", encoding="utf-8") as file:
        file.write(data)
        file.flush()               # Vider le buffer Python
        os.fsync(file.fileno())    # Vider le buffer OS (très important)
    
    os.replace(tmp_path, file_path)  # Remplace de façon atomique (sûre)



"""
Faut utiliser pickle

def save_bin(file_path: str, data: ) -> None:
    "" Save data in a file ""
    file_path = file_path.replace("\\","/")
    tmp_path = file_path+".tmp"
    
    with open(tmp_path, "wb") as file:
        file.write(data)
        file.flush()               # Vider le buffer Python
        os.fsync(file.fileno())    # Vider le buffer OS (très important)
    
    os.replace(tmp_path, file_path)  # Remplace de façon atomique (sûre)
"""

"""
Faut utiliser pickle
def save_bin(file_path: str, data: ) -> None:
    file_path = file_path.replace("\\","/")
    file = open(file_path,"wb")
    file.write(data)
    file.close()
"""

def read_file(file_path: str) -> str:
    """ Retrieves the content of a file """
    file_path = file_path.replace("\\","/")
    file = open(file_path,"r")
    data = file.read()
    file.close()
    return data

def get_list_of_lines(file_path: str) -> list[str]:
    """ Retrieves the content of a file and split it in all lines """
    file_path = file_path.replace("\\","/")
    file = read_file(file_path)
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
    
    """
    b = {
        "a":1,
        "b":2,
        "c":3
    }
    b = "Hello World"
    save_bin("./working_progress/file.log",b"https://i.ytimg.com/vi_webp/dQw4w9WgXcQ/maxresdefault.webp")
    """
    #print(get_json("D:/Programation/Python/Youtube_Download/history/Error_2025_06_09.log"))
    save_file(r"./tmp/test.txt","test")
