import os
import shutil
import re

def move_and_delete_logs(log_file_path, success_directory):
    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    for line in lines:
        if "Successfully processed and updated:" in line:
            match = re.search(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) - Successfully processed and updated: (.+)', line)
            if match:
                timestamp, file_path = match.groups()
                subdirectory_name = os.path.basename(os.path.dirname(file_path))
                target_directory = os.path.join(success_directory, subdirectory_name)
                target_file_path = os.path.join(target_directory, os.path.basename(file_path))
                os.makedirs(target_directory, exist_ok=True)
                shutil.move(file_path, target_file_path)
                print("Done")
    os.remove(log_file_path)
    os.remove('redditComments.txt')

log_file_path = 'processing_log.txt'
success_directory = './Reddit/successComments/'

move_and_delete_logs(log_file_path, success_directory)
