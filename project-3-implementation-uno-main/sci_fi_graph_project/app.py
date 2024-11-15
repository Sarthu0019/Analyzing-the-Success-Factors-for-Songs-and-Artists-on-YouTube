from flask import Flask, render_template, request, redirect, url_for
from graphCode.newsGraph import getNewsData
from graphCode.redditCommentsPostsGraph import getRedditGraphData
from graphCode.extractYouTube import getChannelData
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd
from datetime import datetime

allChannelData = [['Lady Gaga', 'UCNL1ZadSjHpjm4q9j2sVtOA', 'ladygaga'], ['Kid Cudi', 'UCoNPsL8j28yfKRu6e7YUhPA', 'kidcudi'], ['Fall Out Boy', 'UC2qWxZHgnlwDvcmLqP23jrA', 'falloutboy'], ['Death Grips', 'UCuq1H-HXWoW4JL-hX5bWxzw', 'deathgrips'], ['David Bowie', 'UC8YgWcDKi1rLbQ1OtrOHeDw', 'davidbowie'], ['Kanye West', 'UCs6eXM7s8Vl5WcECcRHc2qQ', 'kanye'], ['Odd Future - Topic', 'UC7V34pJZN9v7J1eLp4uq9Jg', 'ofwgkta'], ['Blonded', 'UCqf-kTp9ERV5T1rPayno7LA', 'fleetwoodmac'], ['The Weeknd', 'UC0WP5P-ufpRfjbNrmOWwLBQ', 'theweeknd'], ['Michael Jackson', 'UC5OrDvL9DscpcAstz7JnQGA', 'michaeljackson'], ['Gorillaz', 'UCfIXdjDQH9Fau7y99_Orpjw', 'gorillaz'], ['Grateful Dead', 'UCPuuuhmMW7jh6roOrIV9yRw', 'gratefuldead'], ['The Rolling Stones', 'UCB_Z6rBg3WW3NL4-QimhC2A', 'rollingstones'], ['The Beatles', 'UCc4K7bAqpdBP8jh1j9XZAww', 'beatles'], ['Chance The Rapper', 'UCeXp3EC97_rUl_e2vgM3gLg', 'chancetherapper'], ['Daft Punk', 'UC_kRDKYrUlrbtrSiyu5Tflg', 'daftpunk'], ['blink-182', 'UCdvlHk5SZWwr9HjUcwtu8ng', 'blink182'], ['Taylor Swift', 'UCqECaJ8Gagnn7YCbPEzWH6g', 'taylorswift'], ['Coldplay', 'UCDPM_n1atn2ijUwHd0NNRQw', 'coldplay'], ['TOOL', 'UC1wUo-29zS7m_Jp-U_xYcFQ', 'toolband'], ['Metallica', 'UCbulh9WdLtEXiooRcYK7SWw', 'metallica'], ['Lana Del Rey', 'UCqk3CdGN_j8IR9z4uBbVPSg', 'lanadelrey'], ['Pink Floyd', 'UCY2qt3dw2TQJxvBrDiYGHdQ', 'pinkfloyd'], ['BROCKHAMPTON', 'UCFLnwFhuJeBSCjIJewxSqKw', 'brockhampton'], ['EminemMusic', 'UCfM3zsQsOnfWNUppiycmBuw', 'eminem'], ['twenty one pilots', 'UCBQZwaNPFfJ1gZ1fLZpAEGw', 'twentyonepilots'], ['pgLang', 'UCZwYLLsXM2rBtixxFAdYR1A', 'kendricklamar'], ['AC/DC', 'UCB0JSO6d5ysH2Mmqz5I9rIw', 'acdc'], ['Official Arctic Monkeys', 'UC-KTRBl9_6AX10-Y7IKwKdw', 'arcticmonkeys'], ['Fleetwood Mac', 'UCAb60rVrvVQVfSgrX1UWb0g', 'fleetwoodmac'], ['Prince', 'UCv3mNSNjuWldihk1DUdnGtw', 'prince'], ['XXXTENTACION', 'UCM9r1xn6s30OnlJWb-jc3Sw', 'xxxtentacion'], ['ALL', 'ALL', 'ALL']]


app = Flask(__name__)

def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='#30303a').generate(text)
    buffer = BytesIO()
    wordcloud.to_image().save(buffer, format='PNG')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.read()).decode('utf-8')
    return image_data

@app.route('/news', methods=['GET', 'POST'])
def news():
    labels, values, totalNewsCount, celebCountDict, newsHeadings = getNewsData()
    try:
        startDate = request.form['startDate']
        endDate = request.form['endDate']
    except:
        startDate, endDate = celebCountDict[0]['date'], celebCountDict[-1]['date']
        
    for i in range(len(celebCountDict)):
        if celebCountDict[i]['date'] == startDate:
            startIndex = i
        if celebCountDict[i]['date'] == endDate:
            endIndex = i
    
    words = []
    for i in range(startIndex, startIndex + len(newsHeadings[startIndex:endIndex+1])):
        words.append(" ".join(newsHeadings[i]))
    wordcloud_image = generate_wordcloud(" ".join(words))

    return render_template('news.html', labels=labels, values=values, totalNewsCount=totalNewsCount, celebCountDict=celebCountDict[startIndex:endIndex+1], startDate=startDate, endDate=endDate, wordcloud_image=wordcloud_image)

@app.route('/redditComments', methods=['GET', 'POST'])
def redditComments():
    try:
        celebName = request.form['celebName']
        totalComments, totalPosts, startDate, endDate, allDates, allComments, allPosts, allCelebNames = getRedditGraphData(celebName)
        startDate, endDate = request.form['startDate'], request.form['endDate']
    except:
        celebName = 'acdc'
        totalComments, totalPosts, startDate, endDate, allDates, allComments, allPosts, allCelebNames = getRedditGraphData(celebName)
    
    mergedData = pd.concat([totalComments.set_index('date'), totalPosts.set_index('date')], axis=1, join='outer')
    mergedData = mergedData.fillna(0)
    mergedData = mergedData.reset_index()
    mergedData = mergedData[(mergedData['date'] >= startDate) & (mergedData['date'] <= endDate)]
    mergedRecords = mergedData.to_dict(orient='records')
    
    allComments = allComments[(allComments['date'] >= startDate) & (allComments['date'] <= endDate)]
    allComments = allComments['body'].tolist()
    
    allPosts = allPosts[(allPosts['date'] >= startDate) & (allPosts['date'] <= endDate)]
    allPosts = allPosts['title'].tolist()
    
    words = []
    for i in range(len(allComments)): words.append(str(allComments[i]))
    wordcloud_image0 = generate_wordcloud(" ".join(words))
    
    df = pd.read_csv('./Reddit/subscribers.csv')
    df.set_index('celebName', inplace=True)
    dfTrans = df.T
    percentChange = dfTrans.divide(dfTrans.iloc[0]) * 100 - 100
    dataJson = percentChange.to_json(orient='columns')
    
    
    return render_template('redditComments.html', mergedRecords=mergedRecords, startDate=startDate, endDate=endDate, allDates=allDates, allCelebNames=allCelebNames, currentSelebName=celebName, wordcloud_image0=wordcloud_image0, dataJson=dataJson)

@app.route('/youTube', methods=['GET', 'POST'])
def youTube():
    df = pd.read_csv('./YouTube/collectedData/allChannelDetails.csv')
    channelData = allChannelData.copy()
    try:
        currentCeleb1Name = request.form['channelIdSelect']
        currentCeleb2Name = request.form['channelId2Select']
    except:
        currentCeleb1Name = channelData[0][1]
        currentCeleb2Name = channelData[0][1]
        
    dataLeft = getChannelData(currentCeleb1Name)
    dataRight = getChannelData(currentCeleb2Name)
    
    return render_template('youTube.html', dataLeft=dataLeft, dataRight=dataRight, channelData=channelData, currentCeleb1Name=currentCeleb1Name, currentCeleb2Name=currentCeleb2Name)

@app.route('/youTubeLikeViews', methods=['GET', 'POST'])
def youTubeLikeViews():
    channelData = allChannelData.copy()
    try:
        currentCeleb1Name = request.form['channelIdSelect']
    except:
        currentCeleb1Name = channelData[0][1]

    data = getChannelData(currentCeleb1Name)
    
    # print(channelData)
    return render_template('youTubeLikeViews.html', data=data, channelData=channelData, currentCeleb1Name=currentCeleb1Name)

@app.route('/youTubeReddit', methods=['GET', 'POST'])
def youTubeReddit():
    df = pd.read_csv('./YouTube/collectedData/allChannelDetails.csv')
    channelData = allChannelData.copy()
    try:
        currentCeleb1Name = request.form['channelIdSelect']
    except:
        currentCeleb1Name = channelData[0][1]
        
    artistReddit = ""
    for i in range(len(channelData)):
        if channelData[i][1] == currentCeleb1Name:
            artistReddit = channelData[i][2]
            
        
    filePath = f'./Reddit/comments/{artistReddit}.csv'
    df = pd.read_csv(filePath)
    commentCount = df['date'].value_counts().reset_index()
    commentCount.columns = ['date', 'count']
    commentCount = commentCount.sort_values(by='date').reset_index(drop=True)

    data = getChannelData(currentCeleb1Name)
    # print(data)
    tempData = data.copy()

    # Group by date and sum the view counts for each date
    totalViews = tempData.groupby('date')['viewCount'].sum().reset_index()
    totalViews['videoID'] = 'ALL'
    totalViews['videoTitle'] = 'ALL'
    data = pd.concat([data, totalViews], ignore_index=True)

    # print(total_view_count_by_date)
    return render_template('youTubeReddit.html', data=data, channelData=channelData, currentCeleb1Name=currentCeleb1Name, commentCount=commentCount)

@app.route('/redditHateSpeech', methods=['GET', 'POST'])
def redditHateSpeech():
    data = pd.read_csv('./Reddit/commentHateCount.csv')
    data = data.sort_values(by='date', ascending=True)
    userData1 = pd.read_csv('./Reddit/commentsUserIDCount.csv')
    userData2 = pd.read_csv('./Reddit/hateUserIDCount.csv')
    
    return render_template('redditHateSpeech.html', data=data, userData1=userData1, userData2=userData2)

@app.route('/')
def index():
    return render_template('index.html')
    # return redirect(url_for('news'))
    # return redirect(url_for('redditComments'))
    # return redirect(url_for('youTube'))
    # return redirect(url_for('youTubeLikeViews'))
    return redirect(url_for('redditHateSpeech'))




if __name__ == '__main__':
    app.run(debug=True)

