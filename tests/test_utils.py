from utils import Channel
from utils import Video
from utils import PLVideo
from utils import get_service
import pytest
import os
from googleapiclient.discovery import build
import json
from dotenv import load_dotenv, find_dotenv


@pytest.fixture
def channel():
    return Channel(ch_id='UCMCgOm8GZkHp8zJ6l7_hIuA')

@pytest.fixture
def video():
    return Video(id='9lO06Zxhu88')

@pytest.fixture
def plv_video():
    return PLVideo(id='BBotskuyw_M', id_playlist ='PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')



def test_str(channel):
    """тестирует СТР"""
    assert channel.__str__() == "вДудь"


def test_title(channel):
    """тестирует геттер title"""
    assert channel.title == 'вДудь'


def test_description(channel):
    """тестирует геттер description"""
    assert channel.description == 'Здесь задают вопросы'


def test_link(channel):
    """тестирует геттер link"""
    assert channel.link == '@vdud'


def test_subs(channel):
    """тестирует геттер subs"""
    assert channel.subs == '1947591121'


def test_videos(channel):
    """тестирует геттер videos"""
    assert channel.videos == '164'


def test_views(channel):
    """тестирует геттер views"""
    assert channel.views == '1947591121'

def test_str_video(video):
    assert video.__str__() == 'Как устроена IT-столица мира / Russian Silicon Valley (English subs)'

def test_str_plv(plv_video):
    assert plv_video.__str__() == 'Пушкин: наше все? (Литература)'