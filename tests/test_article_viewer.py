import pytest
import re
from bs4 import BeautifulSoup
from article_viewer import PTTArticleViewer

@pytest.fixture
def instance():
    return PTTArticleViewer(headers = { 'cookie': 'over18=1;' })

@pytest.fixture
def article1(instance):
    instance.get('https://www.ptt.cc/bbs/Gossiping/M.1119243418.A.790.html')
    return instance

def test_instance(instance):
    assert isinstance(instance, PTTArticleViewer)

def test_meta(article1):
    assert article1.author() == 'MCI (步步步步步步步步)'
    assert article1.title() == 'Re: (問題)華航空難留言'
    assert article1.datetime() == 'Mon Jun 20 13:04:48 2005'
    assert article1.author_ip() == '220.137.87.186'
    assert article1.meta() == {
        'author': 'MCI (步步步步步步步步)',
        'title': 'Re: (問題)華航空難留言',
        'datetime': 'Mon Jun 20 13:04:48 2005',
        'author_ip': '220.137.87.186'
    }

