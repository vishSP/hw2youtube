import pytest

from utils import Channel
from utils import PLVideo
from utils import PlayList
from utils import Video


@pytest.fixture
def channel():
    return Channel(ch_id='UCMCgOm8GZkHp8zJ6l7_hIuA')


@pytest.fixture
def video():
    return Video(id='9lO06Zxhu88')


@pytest.fixture
def plv_video():
    return PLVideo(id='BBotskuyw_M', id_playlist='PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')


@pytest.fixture
def playList():
    return PlayList(id='PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')


@pytest.fixture
def video_error():
    return Video(id='broken_video_id')


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


def test_url(playList):
    assert playList.url == 'https://www.youtube.com/playlist?list=PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb'


def test_title(playList):
    assert playList.title == 'Редакция. АнтиТревел'


def test_get_ids(playList):
    assert playList.get_ids == ['4jRSy-_CLFg', 'XG6pQ9n4kr0', 'cIs7N8B300M', 'S7Ri5-9WHQY', '9Bv2zltQKQA']


def test_total_duration(playList):
    assert playList.total_duration.__str__() == '3:41:01'


def test_show_best_video(playList):
    assert playList.show_best_video() == "https://youtu.be/9Bv2zltQKQA"


def test_broken_video(video_error):
    assert video_error.title is None
    assert video_error.likes is None
    assert video_error.views is None

