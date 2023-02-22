import os
from googleapiclient.discovery import build
import json
from dotenv import load_dotenv, find_dotenv

"""скрываю АПИ"""
load_dotenv(find_dotenv())
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")


def get_service():
    """получает сервис по api!"""
    load_dotenv(find_dotenv())
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
    service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    return service


class Channel:
    """инициализация по id"""

    def __init__(self, ch_id):
        self.ch_id = ch_id
        self.__ch_info = get_service().channels().list(id=ch_id, part='snippet,statistics').execute()
        self.__title = self.title

    def __str__(self) -> str:
        """Выводит название канала"""
        return f'{self.title}'

    def __add__(self, other) -> int:
        """Складывет кол-во подписчиков"""
        return print(self.subs + other.subs)

    def __lt__(self, other) -> str:
        """Сравнивает количетсво подписчиков"""
        if self.subs > other.subs:
            return True
        else:
            return False

    def to_json(self, filename):
        """Отправляет информацию в джисон"""
        channel_id = self.ch_id
        data = get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)

    @property
    def title(self) -> str:
        """Геттер title"""
        channel_title = self.__ch_info.get('items')[0].get('snippet').get('title')
        return channel_title

    @property
    def description(self):
        """Геттер description"""
        channel_description = self.__ch_info.get('items')[0].get('snippet').get('description')
        return channel_description

    @property
    def link(self):
        """Геттер link"""
        channel_link = self.__ch_info.get('items')[0].get('snippet').get('customUrl')
        return channel_link

    @property
    def subs(self) -> int:
        """Геттер subs"""
        channel_subs = self.__ch_info.get('items')[0].get('statistics').get('viewCount')
        return channel_subs

    @property
    def videos(self) -> int:
        """Геттер videos"""
        channel_videos = self.__ch_info.get('items')[0].get('statistics').get('videoCount')
        return channel_videos

    @property
    def views(self):
        """Геттер views"""
        channel_views = self.__ch_info.get('items')[0].get('statistics').get('viewCount')
        return channel_views

    def print_info(self):
        """выводит инфу о канале"""
        channel_id = self.ch_id
        channel = get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        print(channel)

