import threading
#    ----    ----
import settings_manager as set
import downloader as dl
import history as his


class DowloadManager:
    def __init__(self):
        self.history,self.history_file = his.today_history_get()
    
    def progressbar_manager(self,progressbar):  
        progressbar.start()
    
    def history_manager(self,url,info_video):
        history = {}
        history = his.save_history_converter(self.history,url,info_video)
        his.save_history(history=history,history_file=self.history_file)
    
    def download_and_save_launch_in_thread(self,settings,url,stop_progressbar):
        info_video = dl.get_url_info(url)
        
        # ici il faut afficher la miniature
        
        download_ops = set.convert_settings_for_yt_dlp_sub(settings,url)
        dl.launch_download_sub(download_ops,stop_progressbar)
        
        self.history_manager(url,info_video)
    
    def download_and_save_threads_manager(self,settings,url,start_progressbar,stop_progressbar):
        try :
            print("get_search")
            #print(f"progressbar = {progressbar}")
            #start_progressbar()
            """th1 = threading.Thread(target=start_progressbar)
            th1.start()"""
            #time.sleep(2)
            
            start_progressbar()
            thread = threading.Thread(target=lambda: self.download_and_save_launch_in_thread(
                                                        settings,
                                                        url,
                                                        stop_progressbar
                                                        ))
            thread.start()
            
            """th1 = threading.Thread(target=lambda : self.history_manager(url))
            th1.start()"""
            
            #download_ops = set.convert_settings_for_yt_dlp_sub(settings,url)
            #th2 = threading.Thread(target=lambda : dl.launch_download_sub(download_ops,stop_progressbar))
            #th2.start()
            
            
        except Exception as e:
            stop_progressbar()
            print("échec !!!!!!!!!!!!!!!!!!!!!!     ", e)

if __name__ == "__main__":
    d = DowloadManager()
    info_video = dl.get_url_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    d.history_manager("https://www.youtube.com/watch?v=dQw4w9WgXcQ",info_video)