import os
import time


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