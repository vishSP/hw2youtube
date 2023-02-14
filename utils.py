import os
from googleapiclient.discovery import build
import json
from dotenv import load_dotenv, find_dotenv
"""скрываю АПИ"""
load_dotenv(find_dotenv())
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

"""получает сервис по api"""
def get_service():
    load_dotenv(find_dotenv())
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
    service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    return service


class Channel:
    """инициализация по id"""
    def __init__(self, ch_id):
        self.ch_id = ch_id
    """выводит инфу о канале"""
    def print_info(self):
        channel_id = self.ch_id
        channel = get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        print(channel)


vdud = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')
vdud.print_info()