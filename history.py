import os
import datetime
import json_controler as json

def today_history_get():
    x = datetime.datetime.now()
    
    history_file = x.strftime("%x").replace("/","-")
    history_file = list(history_file)
    history_file[0:2],history_file[3:5] = history_file[3:5], history_file[0:2]
    history_file.insert(6,"20")
    history_file = "".join(history_file)
    history_file = "./history/"+history_file+".log"
    print(history_file)
    
    if os.path.exists(history_file):
        return json.get_json(history_file), history_file
    else:
        print("file doesn't exist")
        return {}, history_file

def get_current_time():
    x = datetime.datetime.now()
    time = x.strftime("%X").replace("/","-")
    time = list(time)
    time[2],time[5:] = "h","min"
    time.insert(3," ")
    time = "".join(time)
    print(time)
    return(time)

def get_history_number(history={}):
    num = len(history) + 1
    return num

def save_history_converter(history={},url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",video_info={'title': 'Rick Astley - Never Gonna Give You Up (Official Music Video)', 'thumbnail': 'https://i.ytimg.com/vi_webp/dQw4w9WgXcQ/maxresdefault.webp'}):
    time = get_current_time()
    key = get_history_number(history)
    new_history = {
        "thumbnail" : video_info["thumbnail"],
        "title" : video_info["title"],
        "time" : time,
        "url" : url
    }
    history[f"{key}"] = new_history
    return history

def save_history(history_file,history):
    json.save_json(file_name=history_file,data=history)

if __name__ == "__main__":
    #import downloader as dl
    #info,video = dl.get_url_info()
    today_history_get()
    #get_current_time()
    #save_history_converter()
    #print(get_history_number())
    