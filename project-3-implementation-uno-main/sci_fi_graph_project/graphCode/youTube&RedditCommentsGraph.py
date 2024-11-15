import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="darkgrid")

def countComments(filePath):
    try:
        df = pd.read_csv(filePath)
        return len(df)
    except FileNotFoundError:
        return 0

def extractDate(filePath):
    return pd.to_datetime(filePath[-12:-4], format='%Y%m%d', errors='coerce')

def plotComments(redditLog, youtubeLog):
    redditData = pd.DataFrame({
        'Date': [extractDate(date) for date in redditLog],
        'Total Reddit Comments': [countComments(file) for file in redditLog]
    })

    youtubeData = pd.DataFrame({
        'Date': [extractDate(date) for date in youtubeLog],
        'Total YouTube Comments': [countComments(file) for file in youtubeLog]
    })

    totalRedditComments = redditData['Total Reddit Comments'].sum()
    totalYouTubeComments = youtubeData['Total YouTube Comments'].sum()

    print(f"Total Reddit Comments: {totalRedditComments}")
    print(f"Total YouTube Comments: {totalYouTubeComments}")

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Total Reddit Comments', color=color)
    ax1.plot(redditData['Date'], redditData['Total Reddit Comments'], color=color, marker='o', linestyle='-', label='Reddit Comments')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:blue'
    ax2.set_ylabel('Total YouTube Comments', color=color)
    ax2.plot(youtubeData['Date'], youtubeData['Total YouTube Comments'], color=color, marker='*', linestyle='-', label='YouTube Comments')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.xticks(rotation=45, ha='right')

    fig.tight_layout()
    plt.title(f'REDDIT VS YOUTUBE COMMENTS\nTotal Comments Over Time\nReddit Comments: {totalRedditComments}, YouTube Comments: {totalYouTubeComments}'.upper(), fontsize=16, weight="bold")

    plt.show()

redditLogFile = "redditNormalComments.txt"
youtubeLogFile = "youTubeComments.txt"

with open(redditLogFile) as file:
    redditLog = [line.strip() for line in file]

with open(youtubeLogFile) as file:
    youtubeLog = [line.strip() for line in file]

plotComments(redditLog, youtubeLog)
