import pytest
import re
from bs4 import BeautifulSoup
from board_viewer import PttBoardViewer

base_url = 'https://www.ptt.cc/bbs/'
board = 'Beauty'
url = 'https://www.ptt.cc/bbs/Beauty/index.html'
headers = {
    'cookie': 'over18=1;'
}
ptt_board_viewer = PttBoardViewer(headers = headers)

@pytest.fixture
def instance():
    return PttBoardViewer(headers = headers)

def test_instance(instance):
    assert isinstance(instance, PttBoardViewer)

@pytest.mark.parametrize(
    "test_case, expected",
    [
        ('https://www.ptt.cc/bbs/Beauty/index.html', True),
        ('https://ptt.cc/bbs/Beauty/index.html', True),
        ('https://ptt.cc/bbs/Beauty/index132.html', True),
        ('https://www.ptt.cc/bbs/Beauty/index.htmlasd', False)
    ]
)
def test__check_url(instance, test_case, expected):
    assert instance._PttBoardViewer__check_url(test_case) == expected

def test__set_status(instance):
    class Test:
        status_code = 200
        text = ''
    req = Test()
    instance._PttBoardViewer__set_status(url = 'test', req = req)
    assert instance.status['req_url'] == 'test'
    assert instance.status['res_code'] == 200
    assert isinstance(instance.soup, BeautifulSoup)

@pytest.mark.parametrize(
    "test_case, expected",
    [
        ('https://www.ptt.cc/bbs/Beauty/index.html', None),
    ]
)
def test_get(instance, test_case, expected):
    assert instance.get(test_case) == expected
    assert instance.status['req_url'] == test_case
    assert instance.status['res_code'] == 200
    assert isinstance(instance.soup, BeautifulSoup)

@pytest.mark.parametrize(
    "test_case",
    [
        'https://www.ptt.cc/bbs/Beauty/index.htmlasd',
        'https://www.ptt.cc/bbs/Beauty/index12312.html'
    ]
)
def test_get_exception(instance, test_case):
    with pytest.raises(Exception):
        instance.get(test_case)

@pytest.mark.parametrize(
    "test_case, expected",
    [
        ('爆', 100),
        ('', 0),
        ('XX', -100),
        ('X1', -10),
        ('95', 95)
    ]
)
def test__numerate_push(instance, test_case, expected):
    assert instance._PttBoardViewer__numerate_push(test_case) == expected

def test_nav_page(instance):
    instance.get('https://www.ptt.cc/bbs/Beauty/index2.html')
    assert re.match(r'^https:\/\/www\.ptt\.cc\/bbs\/Beauty\/index1\.html$', instance.oldest_page())
    assert re.match(r'^https:\/\/www\.ptt\.cc\/bbs\/Beauty\/index[0-9]+\.html$', instance.prev_page())
    assert re.match(r'https://www.ptt.cc/bbs/Beauty/index3.html', instance.next_page())
    assert re.match(r'https://www.ptt.cc/bbs/Beauty/index.html', instance.newest_page())

def test__is_disable(instance):
    instance.get('https://www.ptt.cc/bbs/Beauty/index1.html')
    assert instance.prev_page() == None
    instance.get('https://www.ptt.cc/bbs/Beauty/index.html')
    assert instance.next_page() == None

def test_get_posts(instance):
    instance.get('https://www.ptt.cc/bbs/Beauty/index.html')
    post_metas = instance.get_posts()
    assert isinstance(post_metas, list)
    assert list(post_metas[0].keys()) == ['url', 'author', 'title', 'date', 'pushNumber']

