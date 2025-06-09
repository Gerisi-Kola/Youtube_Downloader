import threading
#    ----    ----
import settings_manager as set
import downloader as dl
import history as his


class DowloadManager:
    def __init__(self):
        self.history,self.history_file = his.today_history_get()
        self.all_error_log,self.error_log_file = his.today_history_get("Error_")
        print(f"{self.all_error_log=}\n\n{self.error_log_file=}")
        #print(self.error_log,"\n",self.error_log_file)
    
    def progressbar_manager(self,progressbar) -> None:  
        progressbar.start()
    
    def history_manager(self,url: str, info_video: dict) -> None:
        history = his.save_history_converter(self.history,url,info_video)
        his.save_history(history=history,history_file=self.history_file)
    
    def error_history_manager(self,url: str, error: dict) -> None:
        #log = his.save_history_converter(self.error_log,url,error)
        a = his.save_error_history(self.all_error_log,url,error)
        his.save_history(self.error_log_file,a)
        #print("Error saved !!!!!!!!!!!!!!!!!!",print(self.error_log_file))
    
    def download_and_save_launch_in_thread(self, settings: dict, url: str, stop_progressbar) -> None:
        error_info_video,error_yt_dlp_python = "Ok","Ok"
        error_yt_dlp_sub,error_history = "Ok","Ok"
        try:
            try:
                info_video = dl.get_url_info(url)
            except Exception as e:
                error_info_video = e
                #print(error_info_video)
            # ici il faut afficher la miniature
            
            try:
                download_ops_python = set.convert_settings_for_yt_dlp_python(settings)
                dl.launch_download_python(download_ops_python, url, stop_progressbar)
            except Exception as e:
                error_yt_dlp_python = e
                print("Error first download : ", error_yt_dlp_python)
                download_ops_subprocess = set.convert_settings_for_yt_dlp_sub(settings, url)
                dl.launch_download_sub(download_ops_subprocess, stop_progressbar)
            
            try:
                self.history_manager(url, info_video)
            except Exception as e:
                error_history = e
                print(error_history)
            
        except Exception as e:
            error_yt_dlp_sub = e
            print("Error total download : ", error_yt_dlp_sub)
            stop_progressbar(True)
        
        if error_info_video != error_yt_dlp_python or error_yt_dlp_sub != error_history or error_yt_dlp_sub != "Ok":
            time = his.get_current_time()
            new_error = {
                "Time" : time,
                "URL" : url,
            }
            if error_info_video != "Ok" :
                new_error["Get video info "] = str(error_info_video).replace("\"","'")
                
            if error_yt_dlp_python != "Ok" and error_yt_dlp_python != error_info_video:
                new_error["Download with python "] = str(error_yt_dlp_python).replace("\"","'")
                
            if error_yt_dlp_sub != "Ok"  and error_yt_dlp_sub != error_yt_dlp_python:
                new_error["Download with subprocess "] = str(error_yt_dlp_sub).replace("\"","'")
                
            if error_history != "Ok" :
                new_error["Save history "] = str(error_history).replace("\"","'")
            
            #print(new_error)
            self.error_history_manager(url,new_error)
    
    def download_and_save_threads_manager(self,settings: dict, url: str, start_progressbar, stop_progressbar) -> None:
        try :
            start_progressbar()
            thread = threading.Thread(target=lambda: self.download_and_save_launch_in_thread(
                                                        settings,
                                                        url,
                                                        stop_progressbar
                                                        ))
            thread.start()
            
        except Exception as e:
            stop_progressbar()
            print("échec !!!!!!!!!!!!!!!!!!!!!!     ", e)

if __name__ == "__main__":
    d = DowloadManager()
    """info_video = dl.get_url_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    d.history_manager("https://www.youtube.com/watch?v=dQw4w9WgXcQ",info_video)"""