import re
import typing as t
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
            'PUSH': 'div.nrec',
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

        while soups:
            article = soups.pop()
            if self.__is_deleted(article):
                continue

            outputs.append(
                {
                    'board': self._status['looking_for'][0],
                    'url': urljoin(
                        self.BASE_URL,
                        article.select(
                            self.SELECTOR["ARTICLE_META"]["URL"]
                            )[0]["href"]
                    ),
                    'date': article.select(
                        self.SELECTOR["ARTICLE_META"]["DATE"]
                        )[0].text,
                    'author': article.select(
                        self.SELECTOR["ARTICLE_META"]["AUTHOR"]
                        )[0].text,
                    'title': re.escape(
                        article.select(
                            self.SELECTOR["ARTICLE_META"]["TITLE"]
                        )[0].text
                        ),
                    'push': self.__numerate_push(
                        article.select(
                            self.SELECTOR["ARTICLE_META"]["PUSH"]
                        )[0].text
                        )
                }
                )

        return outputs

    def __is_deleted(self, soup) -> bool:
        return soup.select('div.title > a') == []

    def __numerate_push(self, push: str) -> int:
        if push == '': return 0
        if push == '爆': return 100
        if push == 'XX': return -100
        if push[0] == 'X': return -(int(push[1]) * 10)
        return int(push)