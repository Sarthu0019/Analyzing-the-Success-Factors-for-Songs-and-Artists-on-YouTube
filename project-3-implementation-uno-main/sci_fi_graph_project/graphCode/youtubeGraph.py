import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

sns.set(style="darkgrid")

def parseCommentsData(filePath):
    df = pd.read_csv(filePath)
    totalComments = df.shape[0]
    return {"totalComments": totalComments}

logFilePath = 'youTubeComments.txt'
totalCommentsCounter = 0
commentsData = []

with open(logFilePath, 'r') as logFile:
    for line in logFile:
        csvFilePath = line.strip()
        commentsDate = csvFilePath.split("/")[-1][:-4]
        formatted_date = datetime.strptime(commentsDate, "%Y%m%d").strftime("%Y-%m-%d")

        existingData = next((item for item in commentsData if item["date"] == commentsDate), None)

        if existingData:
            existingData["totalComments"] += parseCommentsData(csvFilePath)["totalComments"]
        else:
            commentsData.append({"date": formatted_date, **parseCommentsData(csvFilePath)})
        
        totalCommentsCounter += parseCommentsData(csvFilePath)["totalComments"]

commentsDf = pd.DataFrame(commentsData)
commentsDf = commentsDf.sort_values(by="date")

plt.figure(figsize=(12, 8))
sns.barplot(x="date", y="totalComments", hue="date", data=commentsDf, palette="viridis", dodge=False, legend=False)

plt.xlabel("Date", fontsize=14)
plt.ylabel("Total Comments", fontsize=14)
plt.title(f"Total Comments Over Time\nTotal Comments: {totalCommentsCounter}".upper(), fontsize=16, weight="bold")
plt.xticks(rotation=45, ha="right")
plt.grid(True)

plt.show()

