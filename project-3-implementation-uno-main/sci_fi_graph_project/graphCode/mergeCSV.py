import os
import pandas as pd

directoryPath = './Reddit/comments/'

def isCsvFileEmpty(filePath):
    return os.path.getsize(filePath) < 10

def mergeCSV(filePath):
    csv_files = [file for file in os.listdir(filePath) if file.endswith('.csv')]
    merged_data = pd.DataFrame()

    for csv_file in csv_files:
        file_path = os.path.join(filePath, csv_file)
        print(f"Processing file: {file_path}")

        if not isCsvFileEmpty(file_path):
            try:
                df = pd.read_csv(file_path)

                if not df.empty:
                    # selected_columns = ['userID', 'title', 'body', 'hate']
                    # df_selected = df[selected_columns]

                    merged_data = pd.concat([merged_data, df], ignore_index=True)
            except Exception as e:
                print(f"Error processing file: {file_path}")
                print(f"Error details: {e}")

    if not merged_data.empty:
        outputFile = "./Reddit/temp/" + filePath.split("/")[-1][:-4] + ".csv"
        merged_data.to_csv(outputFile, index=False)
        print(f'Merged data saved to {outputFile}')
    else:
        print(f'No data to merge in {filePath}')

def foldersInDirectory(filePath):
    folderList = [f for f in os.listdir(filePath) if os.path.isdir(os.path.join(filePath, f))]
    print(folderList)

    for i in range(len(folderList)):
        mergeCSV(directoryPath + folderList[i])

print(foldersInDirectory(directoryPath))


import pandas as pd

myFiles = ['20231109-00', '20231109-12', '20231110-00', '20231110-12', '20231111-00', '20231111-12', '20231112-00', '20231112-12', '20231113-00', '20231113-12', '20231114-00', '20231114-12', '20231115-00', '20231115-12', '20231116-00', '20231116-12', '20231117-00', '20231117-12', '20231118-00', '20231118-12', '20231119-00', '20231119-12', '20231120-00', '20231120-12', '20231121-00', '20231121-12', '20231122-00', '20231122-12', '20231123-00', '20231123-12', '20231124-00', '20231124-12', '20231125-00', '20231125-12', '20231126-00', '20231126-12']

print(len(myFiles))

for i in range(0, len(myFiles)-1,2):
    df1 = pd.read_csv(f'./Reddit/temp/{myFiles[i]}.csv')
    df2 = pd.read_csv(f'./Reddit/temp/{myFiles[i+1]}.csv')

    merged_df = pd.concat([df1, df2], ignore_index=True)
    merged_df.to_csv(f'./Reddit/tempFolder/{myFiles[i][:-3]}.csv', index=False)

    print('Merged data saved to merged_file.csv')


# MERGE REDDIT COMMENTS AND POSTS

#     # # print(logFilePathComments)
#     directory_path = './Reddit/comments/'
#     merged_file_path = 'Reddit/comments/'
    
#     dirPathList = ["20231109-000004","20231109-120004","20231110-000003","20231110-120004","20231111-000003","20231111-120004","20231112-000007","20231112-120004","20231113-000007","20231113-120004","20231114-000003","20231114-120004","20231115-000003","20231115-120004","20231116-000005","20231116-120004","20231117-000004","20231117-120004","20231118-000005","20231118-120004","20231119-000007","20231119-120004","20231120-000005","20231120-120004","20231121-000006","20231121-120004","20231122-000005","20231122-120004","20231123-000004","20231123-120003","20231124-000004","20231124-120004","20231125-000003","20231125-120004","20231126-000004","20231126-120004",]
#     fileNameList = ["20231109_1.csv","20231109_2.csv","20231110_1.csv","20231110_2.csv","20231111_1.csv","20231111_2.csv","20231112_1.csv","20231112_2.csv","20231113_1.csv","20231113_2.csv","20231114_1.csv","20231114_2.csv","20231115_1.csv","20231115_2.csv","20231116_1.csv","20231116_2.csv","20231117_1.csv","20231117_2.csv","20231118_1.csv","20231118_2.csv","20231119_1.csv","20231119_2.csv","20231120_1.csv","20231120_2.csv","20231121_1.csv","20231121_2.csv","20231122_1.csv","20231122_2.csv","20231123_1.csv","20231123_2.csv","20231124_1.csv","20231124_2.csv","20231125_1.csv","20231125_2.csv","20231126_1.csv","20231126_2.csv",]
    
#     # put in cmd
# # copy *09*.csv 20231109.csv

    
#     for j in range(len(dirPathList)):
#         dfs = []

#         for file_name in os.listdir(directory_path + dirPathList[j]):
#             # print(file_name)
#             if file_name.endswith('.csv'):
#                 file_path = os.path.join(directory_path + dirPathList[j], file_name)
#                 try:
#                     df = pd.read_csv(file_path)
#                     if not df.empty:
#                         df['subredditName'] = get_subreddit_name(file_name.split("_")[0])
#                         dfs.append(df)
#                 except:
#                     pass
#         merged_df = pd.concat(dfs, ignore_index=True)

#         merged_df.to_csv(directory_path + fileNameList[j], index=False)

#         print(f'Merged CSV saved to {directory_path + fileNameList[j]}')
    # return 1,2,3,4
