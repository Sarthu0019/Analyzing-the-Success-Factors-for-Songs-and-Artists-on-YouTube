import os
import shutil

log_file_path = 'processing_log.txt'

success_files_dir = './Reddit/collectedData/politics/successComments'

if not os.path.exists(success_files_dir):
    os.makedirs(success_files_dir)

with open(log_file_path, 'r') as log_file:
    for line in log_file:
        if 'Successfully processed and updated' in line:
            try:
                file_path = line.split(':')[-1].strip()
                shutil.move(file_path, os.path.join(success_files_dir, os.path.basename(file_path)))
                print("DONE")
            except:
                pass
                # print(f"Already Done")

print(f'Successfully processed files moved to {success_files_dir}')
