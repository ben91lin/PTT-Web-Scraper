import pytest
import re
from article_viewer import PttArticleViewer

@pytest.fixture
def instance():
    return PttArticleViewer(headers = { 'cookie': 'over18=1;' })\
        .get('https://www.ptt.cc/bbs/Gossiping/M.1119243418.A.790.html')

@pytest.fixture
def RE():
    return {
        'ip': re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'),
        'id': re.compile(r'[a-zA-Z0-9]*'),
        'datetime': re.compile(r'[0-9]{2}\/[0-9]{2}(\s[0-9]{2}\:[0-9]{2})?'),
        'content': re.compile(r'<div class="bbs-screen bbs-content" id="main-content">(.|\n)+</div>'),
        'date': re.compile(r'[0-9]{2}\/[0-9]{2}'),
        'href': re.compile(r'http.+')
    }

def test_instance(instance):
    assert isinstance(instance, PttArticleViewer)

def test_author(instance, RE):
    author = instance.author()
    assert isinstance(author, dict)
    assert list(author.keys()) == ['ip', 'id', 'nickname']
    assert re.match(RE['ip'], author['ip'])
    assert re.match(RE['id'], author['id'])

def test_meta(instance):
    meta = instance.meta()
    assert isinstance(meta, dict)
    assert list(meta.keys()) == ['board', 'url', 'timestamp', 'title', 'push', 'author']
    assert isinstance(meta['timestamp'], float)
    assert isinstance(meta['title'], str)
    assert isinstance(meta['push'], int)
    
def test_content(instance, RE):
    assert re.match(RE['content'], instance.content())

def test_comments(instance, RE):
    comments = instance.comments()
    assert isinstance(comments, list)
    assert isinstance(comments[0], dict)
    assert list(comments[0].keys()) == ['url', 'date', 'tag', 'content', 'commentor']
    assert list(comments[0]['commentor'].keys()) == ['id', 'ip']
    assert re.match(RE['id'], comments[0]['commentor']['id'])
    # Some commenntor doesn't have ip.
    assert re.match(RE['date'], comments[0]['date'])
    assert isinstance(instance.comments()[0]['content'], str)
    assert instance.comments()[0]['tag'] in ['推', '噓', '→']

def test_hrefs(instance, RE):
    instance.get('https://www.ptt.cc/bbs/Beauty/M.1618447251.A.51A.html')
    href = instance.href()
    assert isinstance(href, dict)
    assert list(href.keys()) == ['article', 'comments']
    assert isinstance(href['comments'], list)
    assert isinstance(href['article'], list)
    assert re.match(RE['href'], href['article'][0])