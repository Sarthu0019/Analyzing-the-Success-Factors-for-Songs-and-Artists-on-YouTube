import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

sns.set(style="darkgrid")

def parseLogFile(filePath):
    hateSpeechCountsByDate = {}
    totalComments = 0
    totalHateSpeech = 0

    with open(filePath, "r") as file:
        for line in file:
            parts = line.strip().split("/")[-1]
            parts = parts.replace(".csv", "").split("_")

            dateStr = parts[0]

            date = datetime.strptime(dateStr, "%Y%m%d-%H%M%S")
            date = date.date()

            df = pd.read_csv(line.strip())
            hateSpeechCount = df["HateSpeech"].sum()
            totalComments += len(df)
            totalHateSpeech += hateSpeechCount

            if date in hateSpeechCountsByDate:
                hateSpeechCountsByDate[date] += hateSpeechCount
            else:
                hateSpeechCountsByDate[date] = hateSpeechCount

    return hateSpeechCountsByDate, totalComments, totalHateSpeech

logFilePath = "politicalCommentsMerged.txt"
hateSpeechCountsByDate, totalComments, totalHateSpeech = parseLogFile(logFilePath)

hateSpeechData = pd.DataFrame(list(hateSpeechCountsByDate.items()), columns=["Date", "HateSpeechCount"])
hateSpeechData = hateSpeechData.sort_values(by="Date")

percentHateSpeech = (totalHateSpeech / totalComments) * 100

plt.figure(figsize=(12, 8))
sns.lineplot(x="Date", y="HateSpeechCount", marker="o", data=hateSpeechData, color="r", label="HateSpeech Count")

plt.xlabel("Date", fontsize=14)
plt.ylabel("HateSpeech Count", fontsize=14)
plt.title(f"HateSpeech Count Over Time\nTotal Comments: {totalComments}, Total HateSpeech: {totalHateSpeech}\nPercentage of HateSpeech: {percentHateSpeech:.2f}%".upper(), fontsize=16, weight="bold")
plt.xticks(rotation=45, ha="right")
plt.legend()

plt.grid(True)
plt.show()
