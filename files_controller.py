import json
import os
from pathlib import Path
import shutil
import time
import re
import unicodedata

def remove_backslash(path:str) -> str :
    """ Replace all ' \\ ' by the '/' """
    p = Path(path)
    if path.startswith("./") or path.startswith(".\\"):
        return "./" + p.as_posix()
    else:
        return p.as_posix()

def get_absolut_path(path: str) -> str:
    abs_path = os.path.abspath(path)
    abs_path = remove_backslash(abs_path)
    return abs_path

def get_parent_directory_without_last_slash(path: str) -> str:
    """ Return the parent directory WITHOUT the final '/' """
    p = Path(path)
    if path.startswith("./") or path.startswith(".\\"):
        return "./" + "/".join(p.parts[:-1])
    else:
        return "/".join(p.parts[:-1])
def get_parent_directory(path: str) -> str:
    """ Return the parent directory WITH the final '/' """
    return get_parent_directory_without_last_slash(path) +"/"

def get_json(file_path: str) -> dict | None:
    """ Retrieves data from a json file """
    if os.path.exists(file_path):
        try:
            file_path = file_path.replace("\\","/")
            file = open(file_path,"r")
            data = json.load(file)
            file.close()
            return data
        except json.JSONDecodeError:
            print("Erreur : fichier JSON corrompu ou incomplet.")
            return {}
    else:
        print("The file ",file_path," don't exist")

def get_file_str(file_path: str) -> str:
    """ Retrieves the content of a file """
    file_path = remove_backslash(file_path)
    try:
        file = open(file_path,"r")
        data = file.read()
        file.close()
        return data
    except FileNotFoundError:
        raise Exception("FileNotFoundError : 'get_file_str' : ",file_path," don't exist")

def get_list_of_lines(file_path: str) -> list[str] | None:
    """ Retrieves the content of a file and split it in all lines """
    file_path = remove_backslash(file_path)
    if os.path.exists(file_path):
        with open(file_path, "r") as file: #, encoding="utf-16"
            lignes = [line.strip() for line in file]
        return lignes
    else:
        print("The file ",file_path," don't exist")

def get_file_name_from_path(path: str) -> str:
    p = Path(path)
    return p.name

def get_size_str(src:str) -> str:
    """ Return the size with the units (ex: 1.56 Go) """
    size = get_size(src)
    return convert_size(size)

def get_size(src:str) -> int:
    """ Return the size in octet """
    try:
        size = os.path.getsize(src)
    except:
        try:
            src = remove_backslash(src)
            size = os.path.getsize(src)
        except FileNotFoundError:
            raise Exception("Error 'get_size': ",src," doesn't exist")
    
    return size

def convert_size(size:int) -> str:
    """ Convert the size from octet to Go, Mo, ko """
    if size > 1000000000 :
        size = str(round(size/1000000000,2)) + " Go"
    elif size > 1000000:
        size = str(round(size/1000000,2)) + " Mo"
    elif size > 1000:
        size = str(round(size/1000,2)) + " ko"
    else:
        size = str(size) + " o"
    return size

def change_suffix_if_need(file: str, suffix: str) -> str :
    """ If the file don't finish correctly, change it (ex: ./file.png -> ./file.jpg)"""
    path, old_suffix = os.path.splitext(file)
    return path + suffix

def save_json(file_path: str, data: dict, tmp_path="") -> None:
    """ Save data in a json file """
    file_path = remove_backslash(file_path)
    if tmp_path == "":
        tmp_path = file_path+".tmp"
    create_parent_directory_if_not_exist(file_path)
    
    with open(tmp_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4,ensure_ascii=False)
        file.flush()               # Vider le buffer Python
        os.fsync(file.fileno())    # Vider le buffer OS (très important)
    
    os.replace(tmp_path, file_path)  # Remplace de façon atomique (sûre)
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

def save_file(file_path: str, data: str, tmp_path="") -> None:
    """ Save data in a file """
    file_path = remove_backslash(file_path)
    if tmp_path == "":
        tmp_path = file_path+".tmp"
    create_parent_directory_if_not_exist(file_path)
    
    with open(tmp_path, "w", encoding="utf-8") as file:
        file.write(data)
        file.flush()               # Vider le buffer Python
        os.fsync(file.fileno())    # Vider le buffer OS (très important)
    
    os.replace(tmp_path, file_path)  # Remplace de façon atomique (sûre)

def create_file_if_not_exist(file_path: str) -> None:
    """ Search if file exists. If it don't exist, create it """
    file_path = remove_backslash(file_path)
    if not os.path.exists(file_path):
        _create_parent_directory_if_not_exist(file_path)
        file = open(file_path, 'x')
        file.close()

def _create_directory_if_not_exist(directory_path: str) -> None:
    """ Without remove_backslash : Search if directory exists. If it don't exist, create it """
    _create_parent_directory_if_not_exist(directory_path)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
def create_directory_if_not_exist(directory_path: str) -> None:
    """ Search if directory exists. If it don't exist, create it """
    _create_directory_if_not_exist(remove_backslash(directory_path))

def _create_parent_directory_if_not_exist(directory: str) -> None:
    if not os.path.exists(directory):
        parent_directory = get_parent_directory(directory)
        if os.path.exists(parent_directory):
            _create_directory_if_not_exist(parent_directory)
        else:
            _create_parent_directory_if_not_exist(parent_directory)
def create_parent_directory_if_not_exist(directory: str) -> None:
    _create_parent_directory_if_not_exist(remove_backslash(directory))

def remove_file_if_exist(file_path: str) -> None:
    """ Remove file if it exists """
    file_path = remove_backslash(file_path)
    if os.path.exists(file_path):
        os.remove(file_path)

def remove_empty_directory_if_exist(path: str) -> None:
    """ Remove empty directory if it exists """
    path = remove_backslash(path)
    if os.path.exists(path) and os.path.isdir(path):
        if os.listdir(path) == []:
            os.removedirs(path)

def remove_directory_if_exist(path: str) -> None:
    """ Remove directory if it exists """
    try:
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=False)
    except:
        path = remove_backslash(path)
        if os.path.exists(path):
            shutil.rmtree(path, ignore_errors=False)

def rename_file_correctly_if_need(path:str) -> str:
    """ input path and output new_path"""
    print(f"{path=}")
    file = get_file_name_from_path(path)
    name, suffix = os.path.splitext(file)
    # True si il y a des character autres que - et _ et 0-9 et a-z et A-Z
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", name):
        dest = rename_file_correctly(path)
        print(dest)
        return dest
    return path

def rename_file_correctly(src: str) -> str:
    assert type(src) == str, f"Error 'rename_file_correctly' : {src} is not a str"
    p = Path(src)
    # Séparer le nom et l'extension
    name = p.name.split('.')[0] # nom sans multi extension : file.png.jpeg -> file
    suffix = p.suffix
    
    # Normaliser les caractères Unicode (é → e)
    name = unicodedata.normalize("NFKD", name)
    name = name.encode("ascii", "ignore").decode("ascii")
    
    # Remplacer séparateurs multiples
    name = re.sub(r"[\\/]+", "/", name)
    
    # Remplacer caractères spéciaux par ""
    name = re.sub(r"[^a-zA-Z0-9./_-]", "", name)
    
    # Cas spécial : "_-_" → "-"
    name = re.sub(r"_+-_+", "-", name)
    
    # Nettoyage des fins parasites (--, __, ..)
    name = re.sub(r"[-_.]+$", "", name)
    
    # Compactage, supprime les -- et __ qui se suivent
    name = re.sub(r"[_-]{2,}", lambda m: m.group(0)[0], name)
    
    dst = get_parent_directory(src) + name + suffix
    dst = change_name_if_file_exist(dst)
    dst = remove_backslash(dst)
    _move_file_if_exist(src,dst)
    
    if wait_for_creation(dst):
        remove_file_if_exist(src)
    return dst

def change_name_if_file_exist(file:str) -> str:
    doublon = os.path.exists(file)
    p = Path(file)
    file_name, suffix = p.name,p.suffix
    
    # vérifie si le fichier n'a pas été traiter précédaient
    try:
        index = file_name.rfind("-")
        if index != -1 :
            compteur = int(file_name[index+1:])
        else:
            compteur = 0
    except:
        compteur = 0
    
    while doublon:
        compteur += 1
        new_target = file_name + "-" + str(compteur) + suffix
        doublon = os.path.exists(new_target)
        if not doublon:
            return new_target
    return file

def move_if_exist(src: str, target: str) -> None:
    """ Move the file/directory if it exist"""
    src = remove_backslash(src)
    target = remove_backslash(target)
    _create_parent_directory_if_not_exist(target)
    wait_for_creation(src)
    try:
        os.rename(src,target)
    except FileNotFoundError:
        raise Exception("Error 'move_if_exist': ",src," doesn't exist")

def _move_file_if_exist(src: str, dst: str) -> None:
    """ Move the file/directory if it exist"""
    wait_for_creation(src)
    #assert os.path.isfile(src), f"Error '_move_file_if_exist': {src} is not a file"
    try:
        _create_parent_directory_if_not_exist(dst)
        # ---- ----   Move file   ---- ----
        if os.path.exists(src):
            os.rename(src,dst)
    except FileNotFoundError:
        raise Exception("Error '_move_file_if_exist': ",src," doesn't exist")
def move_file_if_exist (src: str, dst: str) -> None:
    """ Move the file/directory if it exist"""
    _move_file_if_exist(remove_backslash(src),remove_backslash(dst))
rename_file = move_file_if_exist

def move_directory_if_exist(src: str, target: str) -> None:
    """ Move the file/directory if it exist"""
    src = remove_backslash(src)
    wait_for_creation(src)
    try:
        target = remove_backslash(target)
        _create_parent_directory_if_not_exist(target)
        os.rename(src,target)
    except FileNotFoundError:
        raise Exception("Error 'move_directory_if_exist': ",src," doesn't exist")

def copy_file_if_exist(src: str, target: str) -> None:
    """ Move the file if it exist and conserve the metadata (ex: date)"""
    src = remove_backslash(src)
    target = remove_backslash(target)
    _create_parent_directory_if_not_exist(target)
    wait_for_creation(src)
    try:
        assert os.path.isfile(src), f"Error 'copy_file_if_exist': {src} is not a file"
        shutil.copy2(src,target) # 'copy2' copie file fichier avec les metadata 
    except FileNotFoundError:
        raise Exception("Error 'copy_file_if_exist': ",src," doesn't exist")

def copy_modif_time_file(src:str, dst:str) -> None:
    try:
        stat = os.stat(src)
        os.utime(dst, (stat.st_atime, stat.st_mtime))
    except:
        try:
            src = remove_backslash(src)
            dst = remove_backslash(dst)
            wait_for_creation(src)
            stat = os.stat(src)
            os.utime(dst, (stat.st_atime, stat.st_mtime))
        except FileNotFoundError:
            raise Exception("Error 'copy_modif_time_file': ",src," doesn't exist")

def wait_for_creation(src: str, seconds = 1) -> bool | Exception:
    seconds = int(seconds*20)
    for _ in range(seconds):
        if os.path.exists(src):
            return True
        time.sleep(0.05)
    raise Exception(f"Error 'wait_for_creation' : File {src} was not created in {seconds}s")

def wait_for_creation_with_loading(src: str,compt=0, seconds = 2) -> int:
    seconds = int(seconds*40)
    for _ in range(seconds):
        compt = loading(compt)
        if os.path.exists(src):
            return compt
        time.sleep(0.025)
    raise Exception(f"Error 'wait_for_creation' : File {src} was not created in {seconds}s")

def loading(timer:int) -> int:
    """ Simulate the loading """
    max_value = 50
    bar = "█" * 3
    index = max_value - abs(max_value - (timer % (2 * max_value)))
    temp = "-"*(index) + bar + "-"*(max_value-index)
    print(f"\r[{temp}]", end="", flush=True)
    return timer + 1

if __name__ == "__main__":
    p = Path("./test/a.png--.jpeg")
    print(p.stem)
    print(p.suffixes)
    compt = 0
    for i in range(15):
        compt = wait_for_creation_with_loading("a",compt,5)
    #print(rename_file_correctly())