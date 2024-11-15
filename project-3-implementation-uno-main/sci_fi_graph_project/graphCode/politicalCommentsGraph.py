import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns
from datetime import datetime

sns.set(style="darkgrid")

def parseLogFile(filePath):
    dates = []
    commentsCount = []

    with open(filePath, "r") as file:
        for line in file:
            parts = line.strip().split("/")[-1]
            parts = parts.replace(".csv", "").split("_")
            
            dateStr, commentsStr = parts[0], parts[1]

            date = datetime.strptime(dateStr, "%Y%m%d-%H%M%S")

            dates.append(date)
            commentsCount.append(int(commentsStr))

    return dates, commentsCount

logFilePath = "politicalCommentsMerged.txt"
dates, commentsCount = parseLogFile(logFilePath)

hours = [date.hour for date in dates]

fig, myAxis = plt.subplots(figsize=(12, 8))

scatterPlot = myAxis.scatter(dates, commentsCount, c=hours, cmap="viridis", s=50, alpha=0.7)
myAxis.plot_date(dates, commentsCount, "-", color="red", markersize=6, alpha=0.5)

myAxis.set_xlabel("Date", fontsize=14)
myAxis.set_ylabel("Comments Count", color="black", fontsize=14)
myAxis.tick_params("y", colors="red")

colorBar = plt.colorbar(scatterPlot)
colorBar.set_label("Hour of the Day", fontsize=12)

myAxis.xaxis.set_tick_params(rotation=45, labelsize=12)
myAxis.grid(True)

totalComments = sum(commentsCount)
plt.title(f"Dates and Comments Over Time (Binned Hourly)", fontsize=16, weight="bold")
plt.title(f"Dates and Comments Over Time (Binned Hourly)\nTotal Comments: {totalComments}", fontsize=16, weight="bold")

plt.show()
