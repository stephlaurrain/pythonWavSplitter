import os, shutil
import time

def clean_dir(dir_to_clean):                        
                
    for filename in os.listdir(dir_to_clean):
            file_path = os.path.join(dir_to_clean, filename)
            try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                    elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
            except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

def remove_old_files(dir_path, days):
    all_files = os.listdir(dir_path)
    now = time.time()
    n_days = days * 86400
    for f in all_files:
        file_path = os.path.join(dir_path, f)
        if not os.path.isfile(file_path):
            continue
        if os.stat(file_path).st_mtime < now - n_days:
            os.remove(file_path)
            print("Deleted ", f)

def str_to_textfile (filename, str_to_write):
    text_file = open(filename, "w")
    text_file.write(str_to_write)
    text_file.close()