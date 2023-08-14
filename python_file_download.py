#python file download
'''
# python_file_download.py
# created by mahemys; 2023.08.09 10:30 IST
# !perfect, but works!
# GNU-GPL; no license; free to use!
# Update 2023-08-09 12:30 IST; initial review
# 
#------------------------------------------------------------
# purpose
# download multiple files in a loop using python script
# just save all the urls of the files in a text file
# run this program and sit back and enjoy the show!
# internal log writing; time in ist;
# 
#------------------------------------------------------------
# how to use
# just copy file to your location
# run this python script in terminal
# 
#------------------------------------------------------------
# process
# loads urls from text file and download files in a loop
# 
#------------------------------------------------------------
'''
import gc
import os
import time
import requests
from datetime import datetime

dt_start    = datetime.now()
LogDateTime = dt_start.strftime('%Y%m%d_%H%M%S')
print(" ", dt_start, 'start...')

#logs folders; files
out_folder     = 'ext_downloads'   #folder to save downloaded files
inp_file       = 'ext_pending.txt' #text file with all the urls
logs_file_name = out_folder + "_log_" + LogDateTime + ".txt"

try:
    #logs folders; files
    File_path = os.path.abspath(__file__)
    File_dir  = os.path.dirname(__file__)
    Logs_dir  = os.path.join(File_dir, out_folder)
    
    #create folders if not found
    if not os.path.isdir(Logs_dir):
        os.makedirs(Logs_dir)
    logs_file_name = os.path.join(Logs_dir, logs_file_name)
except:
    print(" ", '#Exception: create folder', logs_file_name)
    pass

#logs save as text file
text_file = open(logs_file_name, "w")
text_file.write(logs_file_name + '\n')
text_file.write('\n')

def get_size(path):
    if os.path.exists(path):
        size = os.path.getsize(path)
        if size < 1024:
            return f"{size} bytes"
        elif size < pow(1024,2):
            return f"{round(size/1024, 2)} KB"
        elif size < pow(1024,3):
            return f"{round(size/(pow(1024,2)), 2)} MB"
        elif size < pow(1024,4):
            return f"{round(size/(pow(1024,3)), 2)} GB"
    else:
        return "0 bytes"

def log_write(instance):
    log_text = "{} {}".format(datetime.now(), instance)
    text_file.write(log_text + '\n')
    print(log_text)

def download_url(cur_url, cur_file, cur_count):
    #download function
    chunk_size = 1024 #128
    save_path  = out_folder + "/" + cur_file
    
    if os.path.exists(save_path):
        instance = "{} file exists; skip; size {}; {}".format(cur_count, get_size(save_path), cur_file)
        log_write(instance)
    else:
        try:
            #file not found; download
            r = requests.get(cur_url, stream=True)
            if r.status_code == 200:
                with open(save_path, 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        fd.write(chunk)
                instance = "{} file download; {} saved; size {}; {}".format(cur_count, r.status_code, get_size(save_path), cur_file)
                #print(datetime.now(), cur_count, r.status_code, "saved", cur_file)
            else:
                instance = "{} file download; {} error; size {}; {}".format(cur_count, r.status_code, get_size(save_path), cur_file)
                #print(datetime.now(), cur_count, r.status_code, "error", cur_file)
            log_write(instance)
        except:
            print(" ", '#Exception: file download', cur_file)
            pass
        
        #sleep and take time for next
        time.sleep(1)
        gc.collect()
        
def main_process():
    try:
        #read file
        if not os.path.exists(inp_file):
            instance = "file not found; " + inp_file
            print(instance)
        else:
            f_file   = open(inp_file, 'r')
            url_list = f_file.readlines()
            f_file.close()
            instance = "file found; " + inp_file
            print(instance)
            
            url_count = len(url_list)
            len_count = len(str(url_count))
            print(url_count)
            
            count = 0
            for url in url_list:
                url       = url.strip()
                count     = count+1
                cur_count = str(count).zfill(len_count)
                
                if not "#" in url:
                    #get file name from url
                    cur_url   = url
                    cur_file  = url.split('/')[-1].strip()
                    print(datetime.now(), cur_count, "get", cur_file)
                    
                    #download function
                    download_url(cur_url, cur_file, cur_count)
    except:
        print(" ", '#Exception: file', inp_file)
        pass
    
    #print time taken
    dt_stop = datetime.now()
    dt_diff = (dt_stop - dt_start)
    print(" ", dt_stop, 'all tasks complete...')
    print(" ", 'Time taken {}'.format(dt_diff))
    
    text_file.write('\n')
    text_file.write('Time Start : {}'.format(dt_start) + '\n')
    text_file.write('Time Stop  : {}'.format(dt_stop)  + '\n')
    text_file.write('Time Taken : {}'.format(dt_diff)  + '\n')
    text_file.close()
    
if __name__ == "__main__":
   try:
      main_process()
   except KeyboardInterrupt:
      # do nothing here
      text_file.write("{} - KeyboardInterrupt - Exit...".format(datetime.now()) + '\n')
      text_file.close()
      pass
