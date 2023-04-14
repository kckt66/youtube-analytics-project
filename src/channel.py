import json
import os
from googleapiclient.discovery import build




class Channel:
    """Класс для ютуб-канала"""
    YT_API_KEY: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel = Channel.youtube.channels().list(part='snippet,statistics,contentDetails,topicDetails', id=channel_id)\
            .execute()
        self.title: str = channel['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.sub_count = channel['items'][0]['statistics']['subscriberCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']
        self.info_channel = channel['items'][0]['snippet']['description']

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))


    @classmethod
    def get_service(cls):
        """Класс-метод, возвращающий объект для работы с YouTube API"""
        return cls.youtube


    def to_json(self, name_json):
        """Сохраняет в файл значения атрибутов экземпляра Channel"""
        data = self.__dict__
        with open(name_json, 'w', encoding='utf-8') as file:
            file.write(json.dumps(data, sort_keys=True, indent=3, ensure_ascii=False))
