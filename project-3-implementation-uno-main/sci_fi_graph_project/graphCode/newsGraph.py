import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
sns.set(style="darkgrid")

def parseNewsData(filePath):
    df = pd.read_csv(filePath)
    dateStr = os.path.basename(filePath).split("-")[0]
    date = datetime.strptime(dateStr, "%Y%m%d")
    totalNewsCount = df.shape[0]
    return {"Date": date, "TotalNewsCount": totalNewsCount}


def getNewsData():
    celebNames = ["Kanye West", "gorillaz", "Kendrick Lamar", "Frank Ocean", "Beatles", "Pink Floyd", "Daft Punk", "Eminem", "Taylor Swift", "Death Grips", "GratefulDead", "ToolBand", "Brockhampton", "OFWGKTA", "Metallica", "Lanadelrey", "The Weeknd", "XXXTENTACION", "Coldplay", "Lady Gaga", "FallOutBoy", "Kid Cudi", "David Bowie", "PRINCE", "Michael Jackson", "rollingstones", "Fleetwood Mac", "ACDC", "Blink182", "Chance The Rapper", "Arctic Monkeys", "twenty one pilots",]
    
    dataDirectory = "./News/"
    newsCountsList = []
    celebCountList = []
    newsHeadings = []
    todayHeading = []

    for fileName in os.listdir(dataDirectory):
        todayHeading = []
        if fileName.endswith(".csv"):
            filePath = os.path.join(dataDirectory, fileName)
            newsCount = parseNewsData(filePath)
            newsCountsList.append(newsCount)
            df = pd.read_csv(filePath)

            celeb_counts = {'date': datetime.strptime(fileName[:-11], "%Y%m%d").strftime("%Y-%m-%d")}
            for celeb_name in celebNames:
                celeb_counts[celeb_name] = 0
                
            todayHeading.extend(df['title'].tolist())

            celeb_counts["z All Celebs"] = df.shape[0]

            for celeb_name, count in df['celebName'].value_counts().items():
                celeb_counts[celeb_name] = count

            celebCountList.append(celeb_counts)
            todayHeading = [item for item in todayHeading if isinstance(item, str)]
            newsHeadings.append(todayHeading)

    # newsHeadings = " ".join(newsHeadings)

    newsData = pd.DataFrame(newsCountsList)
    # print(newsData)
    ax = sns.barplot(x="Date", y="TotalNewsCount", hue="Date", data=newsData, palette="viridis", dodge=False, legend=False)
    totalNewsCount = newsData["TotalNewsCount"].sum()

    xValues = [tick.get_text() for tick in ax.get_xticklabels()]
    yValues = [rect.get_height() for rect in ax.patches]

    return xValues, yValues, totalNewsCount, celebCountList, newsHeadings


if __name__ == "__main__":
    
    xValues, yValues, totalNewsCount, celebCountList, newsHeadings = getNewsData()
    print("X values:", xValues)
    print("Y values:", yValues)
    print("Total News Count:", totalNewsCount)
    print("Celeb Count List:", celebCountList)
    print("News Heading List:", newsHeadings)