import datetime
import json
import os

import isodate
from dotenv import load_dotenv, find_dotenv
from googleapiclient.discovery import *

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
    def views(self) -> int:
        """Геттер views"""
        channel_views = self.__ch_info.get('items')[0].get('statistics').get('viewCount')
        return channel_views

    def print_info(self):
        """выводит инфу о канале"""
        channel_id = self.ch_id
        channel = get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        print(channel)


class Video:

    def __init__(self, id):
        self.id = id
        self.__video_info = get_service().videos().list(id=id, part='snippet,statistics').execute()

    def print_info(self):
        """выводит инфу о видео"""
        video_id = self.id
        channel = get_service().videos().list(id=video_id, part='snippet,statistics').execute()
        print(channel)

    @property
    def title(self) -> str:
        """Геттер title"""
        try:
            video_title = self.__video_info.get('items')[0].get('snippet').get('title')
        except:
            return None
        return video_title

    def __str__(self) -> str:
        """Выводит название видео"""
        return f'{self.title}'

    @property
    def views(self) -> int:
        """Геттер views"""
        try:
            video_views = self.__video_info.get('items')[0].get('statistics').get('viewCount')
        except:
            return None
        return video_views

    @property
    def likes(self) -> int:
        """Геттер likes"""
        try:
            video_likes = self.__video_info.get('items')[0].get('statistics').get('likeCount')
        except:
            return None

        return video_likes


class PLVideo(Video):

    def __init__(self, id, id_playlist):
        super().__init__(id)
        self.id_playlist = id_playlist
        self.__playlist_info = get_service().playlists().list(id=id_playlist, part='snippet').execute()

    def __str__(self):
        return f'{super().title} ({self.playlist_name})'

    def print(self):
        """выводит инфу о видео"""
        id_playlist = self.id_playlist
        playlist = get_service().playlists().list(id=id_playlist, part='snippet').execute()
        print(playlist)

    @property
    def playlist_name(self) -> str:
        """Выводит название плейлиста"""
        playlist_title = self.__playlist_info.get('items')[0].get('snippet').get('title')
        return playlist_title


class PlayList:

    def __init__(self, id):
        self.playlist_info = get_service().playlists().list(id=id, part='snippet').execute()
        self.playlist_video_info = get_service().playlistItems().list(playlistId=id, part='snippet,contentDetails',
                                                                      maxResults=50)
        self.video_info = get_service().videos().list(id=id, part='snippet,statistics,contentDetails').execute()
        self.id = id

    @property
    def url(self):
        """выводит ссылку"""
        return (f'https://www.youtube.com/playlist?list={self.id}')

    @property
    def title(self):
        """Выводит название"""
        playlist_title = self.playlist_info.get('items')[0].get('snippet').get('title')
        return playlist_title

    @property
    def get_ids(self):
        """получает список из id"""
        next_page = True
        ids_list = []
        while next_page:
            response = self.playlist_video_info.execute()
            data = response['items']
            for video in data:
                video_id = video['contentDetails']['videoId']
                if video_id not in ids_list:
                    ids_list.append(video_id)

            if 'nextPageToken' in response.keys():
                next_page = True
                self.playlist_video_info = get_service().playlistItems().list(
                    playlistId=id,
                    part='snippet,contentDetails',
                    maxResults=50,
                    pageToken=response['nextPageToken']
                ).execute()
            else:
                next_page = False
        return ids_list

    @property
    def total_duration(self):
        """выводит общее время плейлиста"""
        total_duration = datetime.timedelta(seconds=0)
        list_of_ids = self.get_ids

        for video in list_of_ids:
            video_list = get_service().videos().list(id=video, part='snippet,statistics,contentDetails').execute()
            duration = video_list.get('items')[0].get('contentDetails').get('duration')
            normal_duration = isodate.parse_duration(duration)
            total_duration += normal_duration
        return total_duration

    def show_best_video(self):
        """Вывожу ссылку на самое популярное видео"""
        list_of_ids = self.get_ids

        most = ''
        count = 0

        for video in list_of_ids:
            video_list = get_service().videos().list(id=video, part='snippet,statistics,contentDetails').execute()
            likes = video_list.get('items')[0].get('statistics').get('likeCount')
            likes_fix = int(likes)
            if likes_fix > count:
                count = likes_fix
                most = video

        return f'https://youtu.be/{most}'
