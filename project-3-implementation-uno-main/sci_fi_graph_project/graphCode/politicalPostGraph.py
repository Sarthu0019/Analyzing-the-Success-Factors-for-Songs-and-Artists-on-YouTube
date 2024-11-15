import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from matplotlib.ticker import FuncFormatter

sns.set(style="darkgrid")

def parseLogFile(file_path):
    dates = []
    subscribersCount = []
    totalPostsCount = []

    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split("/")[-1]
            parts = parts.replace(".csv", "").split("_")

            dateStr, subscribersStr, postsStr = parts[0], parts[1], parts[2]

            date = datetime.strptime(dateStr, "%Y%m%d-%H%M%S")

            dates.append(date)
            subscribersCount.append(int(subscribersStr))
            totalPostsCount.append(int(postsStr))

    return dates, subscribersCount, totalPostsCount

logFilePath = "politicalPosts.txt"
dates, subscribersCount, totalPostsCount = parseLogFile(logFilePath)

def formatingToThousand(value, tick_number):
    if value >= 1_000_000:
        return f"{int(value/1_000):,}K"
    elif value >= 1_000:
        return f"{int(value/1_000):,}K"
    else:
        return f"{int(value):,}"

fig, subscriberAxis = plt.subplots(figsize=(12, 8))

sns.lineplot(x=dates, y=subscribersCount, label="Subscribers", color="b", marker="o", markersize=6)

subscriberAxis.set_xlabel("Date and Time", fontsize=14)
subscriberAxis.set_ylabel("Subscribers Count", color="b", fontsize=14)
subscriberAxis.tick_params("y", colors="b")

postAxis = subscriberAxis.twinx()

sns.lineplot(x=dates, y=totalPostsCount, label="Total Posts", color="r", marker="o", markersize=6)

postAxis.set_ylabel("Total Posts Count", color="r", fontsize=14)
postAxis.tick_params("y", colors="r")
subscriberAxis.get_yaxis().set_major_formatter(FuncFormatter(formatingToThousand))
postAxis.get_yaxis().set_major_formatter(FuncFormatter(formatingToThousand))

totalPosts = sum(totalPostsCount)
plt.title(f"Subscribers and Total Posts Over Time".upper(), fontsize=16, weight="bold")
plt.title(f"Subscribers and Total Posts Over Time\nTotal Posts: {totalPosts}".upper(), fontsize=16, weight="bold")
plt.show()
