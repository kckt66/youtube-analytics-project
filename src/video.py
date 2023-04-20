import os
from googleapiclient.discovery import build
import json


class Video:

    YT_API_KEY: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        video = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id)\
            .execute()
        self.title: str = video['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/channel/{self.__video_id}'
        self.view_count = video['items'][0]['statistics']['viewCount']
        self.like_count = video['items'][0]['statistics']['likeCount']


    def __str__(self):
        return self.title



class PLVideo(Video):
    """
    Класс, наследуемый от Video в котором инициализируется id плейлиста
    """
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.playlist_id = playlist_id

