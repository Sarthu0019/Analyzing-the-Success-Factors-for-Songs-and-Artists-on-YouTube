import os
import pandas as pd
import seaborn as sns

sns.set(style="darkgrid")

def parseData(filePath):
    df = pd.read_csv(filePath)
    totalRows = df.shape[0]
    return {"totalRows": totalRows}

def calculate_totals(file_list):
    totals = []
    for file_path in file_list:
        df = pd.read_csv(file_path)
        total_rows = len(df)
        totals.append(total_rows)
    return totals

def get_subreddit_name(fileName):
    return os.path.splitext(fileName)[0]

def getRedditGraphData(celebrity_name):
    directory_path = './Reddit/'
    commentFileLocation = os.path.join(directory_path, "comments", f"{celebrity_name}.csv")
    postFileLocation = os.path.join(directory_path, "posts", f"{celebrity_name}.csv")

    comments_df = pd.read_csv(commentFileLocation)
    posts_df = pd.read_csv(postFileLocation)

    totalComments = comments_df.groupby('date').size().reset_index(name='totalComments')

    totalPosts = posts_df.groupby('date').size().reset_index(name='totalPosts')

    startDate = min(comments_df['date'].min(), posts_df['date'].min())
    endDate = max(comments_df['date'].max(), posts_df['date'].max())

    allDates = pd.concat([comments_df['date'], posts_df['date']]).unique()

    allComments = comments_df[['body', 'date']]
    allPosts = posts_df[['title', 'date']]

    fileNameLoc = get_all_celebrities(directory_path)
    return totalComments, totalPosts, startDate, endDate, allDates, allComments, allPosts, fileNameLoc

def get_all_celebrities(directory_path):
    fileNameLoc = os.listdir(directory_path+"comments/")
    
    for i in range(len(fileNameLoc)):
        fileNameLoc[i] = fileNameLoc[i][:-4]
        
    return fileNameLoc

if __name__ == "__main__":
    directory_path = './Reddit/'
    
    all_celebrities = get_all_celebrities(directory_path)
    print("All Celebrities:", all_celebrities)
