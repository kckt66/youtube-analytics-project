
from datetime import timedelta
import isodate
from googleapiclient.discovery import build
import os



class PlayList:

    YT_API_KEY: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, pl_id):
        """Экземпляр класса инициализируется по id"""
        self.pl_id = pl_id
        self.url = f'https://www.youtube.com/playlist?list={pl_id}'

        self.playlist_response = PlayList.youtube.playlists().list(id=pl_id, part='snippet', maxResults=50)\
            .execute()
        self.title = self.playlist_response['items'][0]['snippet']['title']

        self.get_video = PlayList.youtube.playlistItems().list(playlistId=self.pl_id, part='contentDetails,snippet')\
            .execute()

    @property
    def total_duration(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.get_video['items']]
        video_response = PlayList.youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids))\
            .execute()

        durations = []
        for video in video_response['items']:
            duration_str = video['contentDetails']['duration']
            duration = isodate.parse_duration(duration_str)
            durations.append(duration)

        # Вычисляем общую продолжительность плейлиста
        total_duration = sum(durations, timedelta())

        return total_duration



    def show_best_video(self):
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.get_video['items']]
        videos = PlayList.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_ids)\
            .execute()

        video = videos['items']
        video_likes = {i['id']: i['statistics']['likeCount'] for i in video}

        max_value = max(video_likes, key=lambda k: int(video_likes[k]))

        return f'https://youtu.be/{max_value}'
