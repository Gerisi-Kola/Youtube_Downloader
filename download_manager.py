import threading
import time
#    ----    ----
import settings_manager as set
import downloader as dl
import path
import history as his


class DowloadManager:
    def __init__(self):
        self.history,self.history_file = his.today_history_get()
    
    def progressbar_manager(self,progressbar):
        progressbar.start()
    
    
    def download_and_save(self,settings,url,start_progressbar,stop_progressbar):
        try :
            print("get_search")
            #print(f"progressbar = {progressbar}")
            #start_progressbar()
            """th1 = threading.Thread(target=start_progressbar)
            th1.start()"""
            #time.sleep(2)
            start_progressbar()
            
            download_ops = set.convert_settings_for_yt_dlp_sub(settings,url)
            th2 = threading.Thread(target=lambda : dl.launch_download_sub(download_ops,stop_progressbar))
            th2.start()
            #info = dl.get_url_info(url)
            #history = his.save_history_converter(history,url,info)
            #his.save_history(history=history,history_file=history_file)
        except Exception as e:
            stop_progressbar()
            print("échec !!!!!!!!!!!!!!!!!!!!!!     ", e)