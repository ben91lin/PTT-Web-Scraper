import logging
import re
import requests
import typing as t
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from abstract.board_viewer import BoardViewer
from connection import Connection

class PttBoardViewer(Connection, BoardViewer):
    BASE_URL = 'https://www.ptt.cc'
    SELECTOR = {
        'NAV_BUTTONS': 'div#action-bar-container div.btn-group-paging > a',
        'ARTICLES': 'div.r-list-container div.r-ent',
        'ARTICLE_META': {
            'DATE': 'div.meta > div.date',
            'AUTHOR': 'div.meta > div.author',
            'TITLE': 'div.title > a',
            'PUSH_NUMBER': 'div.nrec',
            'URL': 'div.title > a'
        }
    }

    def __init__(self, headers: dict):
        super().__init__(headers)
            
    def prev_page(self) -> t.Optional[str]:
        soup = self._soup.select(self.SELECTOR["NAV_BUTTONS"])[1]
        if not self.__has_link(soup):
            return None
        else:
            return urljoin(self.BASE_URL, soup["href"])

    def next_page(self) -> t.Optional[str]:
        soup = self._soup.select(self.SELECTOR["NAV_BUTTONS"])[2]
        if not self.__has_link(soup):
            return None
        else:
            return urljoin(self.BASE_URL, soup["href"])

    def has_prev_page(self) -> bool:
        soup = self._soup.select(self.SELECTOR["NAV_BUTTONS"])[1]
        return self.__has_link(soup)

    def has_next_page(self) -> bool:
        soup = self._soup.select(self.SELECTOR["NAV_BUTTONS"])[2]
        return self.__has_link(soup)

    def __has_link(self, soup) -> bool:
        return 'disabled' not in soup['class']

    def oldest_page(self) -> None:
        soup = self._soup.select(self.SELECTOR["NAV_BUTTONS"])[0]
        return urljoin(self.BASE_URL, soup["href"])

    def newest_page(self) -> None:
        soup = self._soup.select(self.SELECTOR["NAV_BUTTONS"])[3]
        return urljoin(self.BASE_URL, soup["href"])

    def articles(self) -> list[dict]:
        soups = self._soup.select(self.SELECTOR['ARTICLES'])
        outputs = []

        for article in soups:
            if self.__is_deleted(article):
                continue

            outputs.append(
                {
                    'url': urljoin(
                        self.BASE_URL,
                        article.select(
                            self.SELECTOR["ARTICLE_META"]["URL"]
                            )[0]["href"]
                    ),
                    'date': article.select(
                        self.SELECTOR["ARTICLE_META"]["DATE"]
                        )[0].text,
                    'author_id': article.select(
                        self.SELECTOR["ARTICLE_META"]["AUTHOR"]
                        )[0].text,
                    'title': re.escape(
                        article.select(
                            self.SELECTOR["ARTICLE_META"]["TITLE"]
                        )[0].text
                        ),
                    'push_number': self.__numerate_push(
                        article.select(
                            self.SELECTOR["ARTICLE_META"]["PUSH_NUMBER"]
                        )[0].text
                        ),
                    'board': self._status['looking_for'][0]
                }
                )

        return outputs

    def __is_deleted(self, soup) -> bool:
        return soup.select('div.title > a') == []

    def __numerate_push(self, push_number: str) -> int:
        if push_number == '爆': return 100
        if push_number == '': return 0
        if push_number == 'XX': return -100
        if push_number[0] == 'X': return -(int(push_number[1]) * 10)
        return int(push_number)