import copy
import logging
import re
import requests
import typing as t
from bs4 import BeautifulSoup
from abstract.article_viewer import ArticleViewer
from connection import Connection

class PTTArticleViewer(Connection, ArticleViewer):
    BASE_URL = 'https://www.ptt.cc'
    SELECTOR = {
        'ARTICLE_META': {
            # In html.parser, the nth-of-type will recaculate article-metaline and article-metaline-right.
            'ALL': 'div.article-metaline, div.article-metaline-right',
            'AUTHOR': 'div.article-metaline:nth-of-type(1) span.article-meta-value',
            'BOARD': 'div.article-metaline-right span.article-meta-value',
            'TITLE': 'div.article-metaline:nth-of-type(3) span.article-meta-value',
            'DATETIME': 'div.article-metaline:nth-of-type(4) span.article-meta-value',
        },
        'CONTENT': 'div#main-content',
        'COMMENTS': 'span.f2 ~ div.push',
        # The richcontent is iframe preview for imgur.com
        'COMMENT_RICHCONTENTS': 'span.f2 ~ div.push ~ .richcontent',
        'COMMENT_META': {
            'TAG': 'push-tag',
            'COMMENTOR': 'push-userid',
            'COMMENT': 'push-content',
            'IPDATETIME': 'push-ipdatetime'
        }
    }
    RE = {
        'ip': re.compile(r'[0-9]{1, 3}\.[0-9]{1, 3}\.[0-9]{1, 3}\.[0-9]{1, 3}'),
        # In PTT, they have two type of ip presentation, 來自: xxx.xxx.xxx.xxx or FROM: xxx.xxx.xxx.xxx
        'author_ip': re.compile(r'((?<=(From\:\s))|(?<=(來自\:\s)))[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'),
        'datetime': re.compile(r'[0-9]{2}\/[0-9]{2}\s[0-9]{2}\:[0-9]{2}')
    }

    def __init__(self, headers: dict):
        super().__init__(headers)

    def meta(self) -> str:
        return {
            'datetime': self.datetime(),
            'author_ip': self.author_ip(),
            'author_id': self.author_id(),
            'author_nickname': self.author_nickname(),
            'title': self.title(),
        }

    def datetime(self) -> str:
        return self._soup.select(self.SELECTOR['ARTICLE_META']['DATETIME'])[0].text

    def author_ip(self) -> str:
        search = re.search(self.RE['author_ip'], self._soup.text)
        return search.group(0) if search else ''

    def author(self) -> str:
        return self._soup.select(self.SELECTOR['ARTICLE_META']['AUTHOR'])[0].text

    def author_id(self) -> str:
        return self.author().split(' (')[0]
    
    def author_nickname(self) -> str:
        return self.author().split(' (')[1].split(')')[0]

    def title(self) -> str:
        return self._soup.select(self.SELECTOR['ARTICLE_META']['TITLE'])[0].text

    def content(self) -> str:
        soup = BeautifulSoup(features = 'html.parser')
        soup.append(copy.copy(self._soup.select(self.SELECTOR['CONTENT'])[0]))
        self.__decompose_comment_richcontents(soup)
        self.__decompose_comments(soup)
        self.__decompose_article_meta(soup)
        return soup.__repr__()

    def __decompose_article_meta(self, selection) -> None:
        article_metas = selection.select(self.SELECTOR['ARTICLE_META']['ALL'])
        for element in article_metas:
            element.decompose()

    def __decompose_comment_richcontents(self, selection) -> None:
        richcontents = selection.select(self.SELECTOR['COMMENT_RICHCONTENTS'])
        for element in richcontents:
            element.decompose()

    def __decompose_comments(self, selection) -> None:
        comments = selection.select(self.SELECTOR['COMMENTS'])
        for element in comments:
            element.decompose()

    def comments(self) -> list[dict]:
        selections = self._soup.select(self.SELECTOR['COMMENTS'])
        outputs = []

        for comment in selections:
            outputs.append(
                {
                    'datetime': self.__datetime(),
                    'tag': comment.select(self.SELECTOR['COMMENT_META']['TAG']),
                    'commentor_id': comment.select(self.SELECTOR['COMMENT_META']['COMMENTOR']),
                    'commentor_ip': self.__commentor_ip(),
                    'comment': comment.select(self.SELECTOR['COMMENT_META']['COMMENT']),
                }
            )

        return outputs

    def __commentor_ip(self, selection):
        '''
        BBS PTT has two kind of board, one display ip address, another none.
        '''
        search = re.search(
            self.RE['ip'],
            selection.select(self.SELECTOR['COMMENT_META']['IPDATETIME'])
            )
        return search.group(0) if search else ''


    def __datetime(self, selection):
        return re.match(
            self.RE['datetime'],
            selection.select(self.SELECTOR['COMMENT_META']['IPDATETIME'])
            ).string

    def medias(self):
        pass