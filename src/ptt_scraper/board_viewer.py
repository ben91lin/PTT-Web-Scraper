import logger
import requests
import typing as t
from bs4 import BeautifulSoup
from abstract.board_viewer import BoardViewer

class PttBoardViewer(BoardViewer):
    BASE_URL = 'https://www.ptt.cc'
    SELECTOR = {
        'NAV_BUTTONS': 'div.#action-bar-container div.btn-group-paging > a',
        'POSTS': 'div.r-list-container div.r-ent',
        'POST_META': {
            'DATE': 'div.meta > div.date',
            'AUTHOR': 'div.meta > div.author',
            'TITLE': 'div.title > a',
            'PUSH_NUMBER': 'div.nrec',
            'URL': 'div.title > a'
        }
    }

    def __init__(self, url: str, headers: dict, BeautifulSoup = BeautifulSoup):
        self.soup = BeautifulSoup(markup = self.__get(url, headers), features = 'html.parser')

    def __get(self, url: str, headers: dict):
        req = requests.get(url, headers = headers)

        if (req.status_code != 200):
            raise Exception(f'The request status is {req.status_code}')
        else:
            return req.text

    def prev_page(self) -> t.Union[None or str]:
        prevElement = self.soup.select(self.SELECTOR.get("NAV_BUTTONS"))[1]
        if self.__is_disable(prevElement):
            return None
        else:
            return f'{self.BASE_URL}{nextElement["href"]}'

    def next_page(self) -> t.Union[None or str]:
        nextElement = self.soup.select(self.SELECTOR.get("NAV_BUTTONS"))[2]
        if self.__is_disable(nextElement):
            return None
        else:
            return f'{self.BASE_URL}{prevElement["href"]}'

    def __is_disable(self, linkSoup) -> bool:
        return 'disabled' in linkSoup['class']

    def oldest_page(self) -> str:
        return f'{self.BASE_URL}{self.soup.select(self.SELECTOR.get("NAV_BUTTONS"))[0]["href"]}'

    def newest_page(self) -> str:
        return f'{self.BASE_URL}{self.soup.select(self.SELECTOR.get("NAV_BUTTONS"))[3]["href"]}'

    def get_posts(self) -> list[dict]:
        posts = self.soup(self.SELECTOR.get('POSTS'))
        postMetas = []

        for post in posts:
            if (self.__is_deleted(post)):
                continue

            date = post.select(self.SELECTOR.get("POST_META").get("DATE"))[0].text
            author = post.select(self.SELECTOR.get("POST_META").get("AUTHOR"))[0].text
            title = self.__regular_title(post.select(self.SELECTOR.get("POST_META").get("TITLE"))[0].text)
            pushNumber = self.__numerate_push(post.select(self.SELECTOR.get("POST_META").get("PUSH_NUMBER"))[0].text)
            url =  f'{self.Domain}{post.select(self.SELECTOR.get("POST_META").get("URL"))[0]["href"]}'

            postMetas.append({'url': url, 'author': author, 'title': title, 'date': date, 'pushNumber': pushNumber})

        return postMetas

    def __is_deleted(self, postSoup) -> bool:
        return postSoup.select('div.title > a') == []

    def __numerate_push(self, pushNumber: t.Union[str or int]) -> int:
        if pushNumber == '爆': return 100
        if pushNumber == '': return 0
        if pushNumber == 'XX': return -100
        if pushNumber[0] == 'X': return -(Int(pushNumber[0]) * 10)
        return pushNumber

    def __regular_title(self, title: str) -> str:
        return re.sub('[\/*?"<>|:"\s\n]', '', title)