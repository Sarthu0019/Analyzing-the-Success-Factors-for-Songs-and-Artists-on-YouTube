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
            file.write(file_path.replace("\\","/") + '\n')


def runThis(whatYouWant):
    allFiles = ["newsData", "youTubeComments", "redditNormalComments", "redditPosts",]
    theirDirectory = ['./News', './YouTube/collectedData/comments', './Reddit/comments', './Reddit/posts',]
    
    index = allFiles.index(whatYouWant)

    all_files = get_all_files_in_directory(theirDirectory[index])
    return all_files
    save_files_to_file(all_files, allFiles[index]+".txt")

    print(f'List of files saved to {allFiles[index]}')  

if __name__ == "__main__":

    runThis("newsData")
    # all_files = get_all_files_in_directory(directoryPath)

    # save_files_to_file(all_files, outputFilePath)

    # print(f'List of files saved to {outputFilePath}')
