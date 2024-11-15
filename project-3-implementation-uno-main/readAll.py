import os

def get_all_files_in_directory(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            all_files.append(file_path)
    return all_files

def save_files_to_file(file_list, output_file):
    with open(output_file, 'w') as file:
        for file_path in file_list:
            file.write(file_path + '\n')

# Replace 'your_directory_path' with the path of the directory you want to scan
directory_path = './News/'
directory_path = './Reddit/splitData'
# directory_path = './YouTube/'
# directory_path = './Testing/'

# Get all files in the directory
all_files = get_all_files_in_directory(directory_path)

# Replace 'output_file.txt' with the desired output file name
output_file_path = 'redditComments.txt'

# Save the list of files to the output file
save_files_to_file(all_files, output_file_path)

print(f'List of files saved to {output_file_path}')
