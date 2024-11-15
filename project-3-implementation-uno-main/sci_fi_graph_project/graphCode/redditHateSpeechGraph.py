import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

sns.set(style="darkgrid")

def parseLogFile(filePath):
    totalCommentsByDate = {}
    totalHateSpeechByDate = {}

    with open(filePath, "r") as file:
        for line in file:
            parts = line.strip().split("/")[-1]
            parts = parts.replace(".csv", "").split("_")

            dateStr = parts[0]

            date = datetime.strptime(dateStr, "%Y%m%d")
            date = date.date()

            df = pd.read_csv(line.strip())
            
            totalComments = len(df)
            if date in totalCommentsByDate:
                totalCommentsByDate[date] += totalComments
            else:
                totalCommentsByDate[date] = totalComments

            totalHateSpeech = (df["HateSpeech"] == True).sum()
            if date in totalHateSpeechByDate:
                totalHateSpeechByDate[date] += totalHateSpeech
            else:
                totalHateSpeechByDate[date] = totalHateSpeech

    return totalCommentsByDate, totalHateSpeechByDate

logFilePath = "redditNormalComments.txt"
totalCommentsByDate, totalHateSpeechByDate = parseLogFile(logFilePath)

data = pd.DataFrame({
    "Date": list(totalCommentsByDate.keys()),
    "TotalRedditComments": list(totalCommentsByDate.values()),
    "TotalHateSpeechComments": list(totalHateSpeechByDate.values())
})
data = data.sort_values(by="Date")

percentHateSpeech = (data["TotalHateSpeechComments"].sum() / data["TotalRedditComments"].sum()) * 100

plt.figure(figsize=(12, 8))
ax1 = sns.lineplot(x="Date", y="TotalRedditComments", marker="o", data=data, color="b", label="Total Reddit Comments")
ax2 = ax1.twinx()
ax2 = sns.lineplot(x="Date", y="TotalHateSpeechComments", marker="*", data=data, color="r", label="Total HateSpeech Comments")

ax1.set_xlabel("Date", fontsize=14)
ax1.set_ylabel("Total Reddit Comments", fontsize=14, color="b")

plt.xticks(rotation=45, ha="right")

ax2.set_ylabel("Total HateSpeech Comments", fontsize=14, color="r")

plt.legend(loc="upper left", bbox_to_anchor=(0.65, 1.0))

plt.title(f"Total Reddit Comments and HateSpeech Comments Over Time\nPercentage of HateSpeech: {percentHateSpeech:.2f}%".upper(), fontsize=16, weight="bold")

plt.grid(True)
plt.show()
