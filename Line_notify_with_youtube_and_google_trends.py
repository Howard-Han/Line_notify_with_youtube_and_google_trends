import requests
from bs4 import BeautifulSoup
import re
import json
import numpy as np
import pandas as pd
from datetime import datetime

#### YT爬蟲
from yt_crawl_210220 import *
YOUTUBE_API_KEY = "你的YOUTUBE_API_KEY"

# 目前已知可用貼圖列表
from line_sticker_ids import *


### message & pic func
def today_google_trends():
    today_date = datetime.now().strftime("%Y%m%d")
    url = "https://trends.google.com.tw/trends/api/dailytrends?hl=zh-TW&tz=-480&ed="+today_date+"&geo=TW&ns=15" # 地區、個數可隨需求調整
    res = requests.get(url)
    test = pd.DataFrame(json.loads(re.sub(r'\)\]\}\',\n', '', res.text))['default']['trendingSearchesDays'][0]['trendingSearches'])
    result_list = []
    for i in range(10):
        aa = "關鍵字第" + str(i+1).zfill(2) + "名: " + test.loc[i,'title']['query']
        bb = aa.ljust(35) + "\n瀏覽比數: " + test.loc[i,'formattedTraffic'] + "\n"
        result_list.append(bb)
    result = ' \n'.join(result_list)
    return result

def get_yt_detail(channel_name, youtube_channel_id, num):
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    # 找頻道資訊與uploads_id
    stat, uploads_id = youtube_spider.get_channel_info(youtube_channel_id)
    # 找前num部影片的id與資訊
    video_ids = youtube_spider.get_playlist(uploads_id, max_results=num)
    vid, published_time, title, views, likes, dislikes, comment_count = [], [], [], [], [], [], []
    for video_id in video_ids:
        video_info = youtube_spider.get_video(video_id)
        vid.append(video_info['id']); published_time.append(video_info['publishedAt']); title.append(video_info['title'])
        views.append(int(video_info['viewCount'])); likes.append(int(video_info['likeCount'])); dislikes.append(int(video_info['dislikeCount'])); comment_count.append(int(video_info['commentCount']))
    ddd = {"vid":vid, "published_time":published_time, "views":views, "likes":likes, "dislikes":dislikes, "comment_count":comment_count, "title":title}
    mydf = pd.DataFrame(ddd)
    # 找近三個月之影片
    mydf['published_time'] = mydf['published_time'].apply(lambda x: x+timedelta(hours=8))
    tt = datetime.now() - timedelta(days=90)
    mydf = mydf[mydf['published_time']>tt]
    mydf.reset_index(drop=True, inplace=True)
    # 標題長度縮減
    mydf['title'] = mydf['title'].apply(lambda x: x[:40])
    # Top 3 觀看數之影片
    mydf.sort_values(by=['views'], ascending=False, inplace=True)
    mydf.reset_index(drop=True, inplace=True)
    mydf = mydf[0:3]
    # 整理成長字串
    stat_string = "頻道名稱: " + channel_name + "\n頻道總觀看數: " + stat['viewCount'] + "\n頻道訂閱數: " + stat['subscriberCount'] + "\n頻道總影片數: " + stat['videoCount']
    video_string = "\n"
    for i in range(3):
        like_dis_ratio = float(np.round((mydf.loc[i,"likes"]/mydf.loc[i,"dislikes"]),2))
        view_com_ratio = float(np.round((mydf.loc[i,"views"]/mydf.loc[i,"comment_count"]),2))
        video_string += "\n"
        video_string += "Top {0} 點閱影片: {1}\n".format(str(i+1), mydf.loc[i,"title"])
        video_string += "觀看數: {0}, 按讚數: {1}, 倒讚數: {2}, 讚-倒讚比: {3}, 留言數: {4}, 觀看-留言比: {5}\n".format(mydf.loc[i,"views"], mydf.loc[i,"likes"], mydf.loc[i,"dislikes"], like_dis_ratio, mydf.loc[i,"comment_count"], view_com_ratio)
    return stat_string+video_string

# get_yt_pic_url()是用來抓youtube影片預覽圖用的，裡面的youtube頻道id可更換成自己喜歡的
def get_yt_pic_url():
    ### 1. 木曜4超玩
    youtube_channel_id = "UCLW_SzI9txZvtOFTPDswxqg"
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    stat, uploads_id = youtube_spider.get_channel_info(youtube_channel_id)
    all_ids = youtube_spider.get_playlist(uploads_id, max_results=20)
    ### 2. 月曜1超玩
    youtube_channel_id = "UCXuzlOCYdY8ox7GUuhVcgjw"
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    stat, uploads_id = youtube_spider.get_channel_info(youtube_channel_id)
    ids_yueyao = youtube_spider.get_playlist(uploads_id, max_results=20)
    all_ids.extend(ids_yueyao)
    ### 3. COVER WINNI
    youtube_channel_id = "UCKPF1g84yaYpOtO2syQ6k1g"
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    stat, uploads_id = youtube_spider.get_channel_info(youtube_channel_id)
    ids_winni1 = youtube_spider.get_playlist(uploads_id, max_results=10)
    all_ids.extend(ids_winni1)
    ### 4. COVER WINNI
    youtube_channel_id = "UCngJawDcrvMgdiyCe8y7dBg"
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    stat, uploads_id = youtube_spider.get_channel_info(youtube_channel_id)
    ids_winni2 = youtube_spider.get_playlist(uploads_id, max_results=10)
    all_ids.extend(ids_winni2)
    ### 5. Lynn
    youtube_channel_id = "UCiewBSUlxrhoyn6oTNt0ilw"
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    stat, uploads_id = youtube_spider.get_channel_info(youtube_channel_id)
    ids_lynn = youtube_spider.get_playlist(uploads_id, max_results=10)
    all_ids.extend(ids_lynn)
    ### 6. Maria
    youtube_channel_id = "UC2tRcusVoXSGqUcSu1GO4Ng"
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    stat, uploads_id = youtube_spider.get_channel_info(youtube_channel_id)
    ids_maria = youtube_spider.get_playlist(uploads_id, max_results=10)
    all_ids.extend(ids_maria)
    ### 抽一個出來
    my_id = str(np.random.choice(all_ids, size=1)[0])
    my_url = "https://i.ytimg.com/vi/"+my_id+"/hq720.jpg"
    return my_url


### Line api func
def lineNotifyMessage(token, msg, n1, n2):
    headers = {
    "Authorization": "Bearer " + token,
    "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message':msg, 'stickerPackageId': n1, 'stickerId':n2}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code
def lineNotifyMessage_pic(token, msg, url):
    headers = {
    "Authorization": "Bearer " + token,
    "Content-Type" : "application/x-www-form-urlencoded"
    }
    payload = {'message':msg, 'imageThumbnail':url, 'imageFullsize':url}
    r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
    return r.status_code



if __name__ == "__main__":
    ### 1. google trends
    token = '你的Line權杖'
    message = today_google_trends()
    message = "\n" + message
    rand = int(np.random.choice(range(344),size=1)[0])
    lineNotifyMessage(token, message, my_list[rand]["STKPKGID"], my_list[rand]["STKID"])
    ### 2. 木曜YT資訊
    token = '你的Line權杖'
    message = get_yt_detail("木曜4超玩", "UCLW_SzI9txZvtOFTPDswxqg", 50) # youtube頻道id可更換成自己喜歡的
    message = "\n" + message
    my_url = get_yt_pic_url()
    lineNotifyMessage_pic(token, message, my_url)
    ### 3. 月曜YT資訊
    token = '你的Line權杖'
    message = get_yt_detail("月曜1起玩", "UCXuzlOCYdY8ox7GUuhVcgjw", 50) # youtube頻道id可更換成自己喜歡的
    message = "\n" + message
    my_url = get_yt_pic_url()
    lineNotifyMessage_pic(token, message, my_url)


