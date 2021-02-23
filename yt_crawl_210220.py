import requests
from datetime import datetime, timedelta
import pandas as pd


YOUTUBE_API_KEY = "AIzaSyBnOdlAn60b7wLEXDq590iAyy0zft2NOZs"


class YoutubeSpider():
    def __init__(self, api_key):
        self.base_url = "https://www.googleapis.com/youtube/v3/"
        self.api_key = api_key
    
    def get_html_to_json(self, path):
        """組合 URL 後 GET 網頁並轉換成 JSON"""
        api_url = f"{self.base_url}{path}&key={self.api_key}"
        r = requests.get(api_url)
        if r.status_code == requests.codes.ok:
            data = r.json()
        else:
            data = None
        return data
    
    def get_channel_info(self, channel_id, part='contentDetails,statistics'):
        # 取得頻道統計資訊, 上傳影片清單的ID
        path = f'channels?part={part}&id={channel_id}'
        data = self.get_html_to_json(path)
        try:
            stat = data['items'][0]['statistics']
            uploads_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        except KeyError:
            stat, uploads_id = None, None
        return stat, uploads_id
        
    def get_playlist(self, playlist_id, part='contentDetails', max_results=10):
        """取得影片清單ID中的影片"""
        path = f'playlistItems?part={part}&playlistId={playlist_id}&maxResults={max_results}'
        data = self.get_html_to_json(path)
        if not data:
            return []
        video_ids = []
        for data_item in data['items']:
            video_ids.append(data_item['contentDetails']['videoId'])
        return video_ids
    
    def get_video(self, video_id, part='snippet,statistics'):
        """取得影片資訊"""
        # part = 'contentDetails,id,liveStreamingDetails,localizations,player,recordingDetails,snippet,statistics,status,topicDetails'
        path = f'videos?part={part}&id={video_id}'
        data = self.get_html_to_json(path)
        if not data:
            return {}
        
        # 以下整理並提取需要的資料
        data_item = data['items'][0]
        try:
            time_ = datetime.strptime(data_item['snippet']['publishedAt'], '%Y-%m-%dT%H:%M:%SZ') # 格凌威志時間
        except ValueError:
            time_ = None
        
        info = {
            'id': data_item['id'],
            'publishedAt': time_,
            'title': data_item['snippet']['title'],
            'viewCount': data_item['statistics']['viewCount'],
            'likeCount': data_item['statistics']['likeCount'],
            'dislikeCount': data_item['statistics']['dislikeCount'],
            'commentCount': data_item['statistics']['commentCount']
        }
        return info


def main():
    ### 1. 木曜4超玩
    youtube_channel_id = "UCLW_SzI9txZvtOFTPDswxqg"
    youtube_spider = YoutubeSpider(YOUTUBE_API_KEY)
    # 找頻道資訊與uploads_id
    stat, uploads_id = youtube_spider.get_channel_info(youtube_channel_id)
    # 找前50部影片的id與資訊
    video_ids = youtube_spider.get_playlist(uploads_id, max_results=50)
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
    # Top 10 觀看數之影片
    mydf.sort_values(by=['views'], ascending=False, inplace=True)
    mydf.reset_index(drop=True, inplace=True)
    mydf = mydf[0:10]
    print(">-------- 木曜4超玩 --------<")
    now_time = datetime.now()
    print("現在時間: ", now_time)
    print("---- 頻道總觀看數: ", stat['viewCount'])
    print("---- 頻道訂閱數: ", stat['subscriberCount'])
    print("---- 頻道總影片數: ", stat['videoCount'])
    print("---- 近三個月觀看數前10名之影片:")
    print(mydf)
    


if __name__ == "__main__":
    main()



