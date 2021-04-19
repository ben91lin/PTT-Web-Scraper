import pytest
import re
from bs4 import BeautifulSoup
from board_viewer import PttBoardViewer

@pytest.fixture
def instance():
    return PttBoardViewer(headers = { 'cookie': 'over18=1;' })

def test_instance(instance):
    assert isinstance(instance, PttBoardViewer)

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
    assert re.match(r'^https:\/\/www\.ptt\.cc\/bbs\/Beauty\/index3\.html$', instance.next_page())
    assert re.match(r'^https:\/\/www\.ptt\.cc\/bbs\/Beauty\/index\.html$', instance.newest_page())

def test__not_has_link(instance):
    instance.get('https://www.ptt.cc/bbs/Beauty/index1.html')
    assert instance.prev_page() == None
    instance.get('https://www.ptt.cc/bbs/Beauty/index.html')
    assert instance.next_page() == None

def test_articles(instance):
    instance.get('https://www.ptt.cc/bbs/Beauty/index.html')
    article_metas = instance.articles()
    assert isinstance(article_metas, list)
    assert list(article_metas[0].keys()) == ['url', 'date', 'author_id', 'title', 'push_number', 'board']

