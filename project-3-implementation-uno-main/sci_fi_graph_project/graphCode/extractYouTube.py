import os
import pandas as pd
from datetime import datetime


def getChannelData(channelName):
    # channelName = "UCB0JSO6d5ysH2Mmqz5I9rIw"
    dfVideos = pd.read_csv('/YouTube/collectedData/allVideoIDs.csv')

    channelData = {}

    for index, row in dfVideos.iterrows():
        channelID = row['channelID']
        videoID = row['videoID']
        videoTitle = row['videoTitle']
    
        if channelID in channelData:
            channelData[channelID][videoID] = { 'videoTitle': videoTitle, 'data': [] }
        else:
            channelData[channelID] = {videoID: { 'videoTitle': videoTitle, 'data': [] }}

    # print(channelData)
    csv_directory = './YouTube/collectedData/dailyData/'

    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(csv_directory, filename)
            df_additional = pd.read_csv(filepath)

            data_date = datetime.strptime(filename.split('-')[0], "%Y%m%d").strftime("%Y-%m-%d")
            for index, row in df_additional.iterrows():
                videoID = row['videoID']

                for channelID, videos in channelData.items():
                    if videoID in videos:
                        channelData[channelID][videoID]['data'].append({
                            'date': data_date,
                            'viewCount': row['viewCount'],
                            'likeCount': row['likeCount'],
                            'commentCount': row['commentCount']
                        })

    # print(channelData)


    data_rows = []
    for videoID, video_info in channelData.get(channelName, {}).items():
        videoTitle = video_info['videoTitle']
        
        for data_entry in video_info.get('data', []):
            data_rows.append({
                'videoID': videoID,
                'date': data_entry['date'],
                'videoTitle': videoTitle,
                'viewCount': data_entry['viewCount'],
                'likeCount': data_entry['likeCount'],
                'commentCount': data_entry['commentCount']
            })
    
    return pd.DataFrame(data_rows)
    print(result_df)


if __name__ == "__main__":
    channelName = "UCB0JSO6d5ysH2Mmqz5I9rIw"
    print(getChannelData(channelName))