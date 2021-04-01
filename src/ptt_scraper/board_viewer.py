import logging
import re
import requests
import typing as t
from bs4 import BeautifulSoup
from abstract.board_viewer import BoardViewer

class PttBoardViewer(BoardViewer):
    BASE_URL = 'https://www.ptt.cc/bbs/'
    SELECTOR = {
        'NAV_BUTTONS': 'div#action-bar-container div.btn-group-paging > a',
        'POSTS': 'div.r-list-container div.r-ent',
        'POST_META': {
            'DATE': 'div.meta > div.date',
            'AUTHOR': 'div.meta > div.author',
            'TITLE': 'div.title > a',
            'PUSH_NUMBER': 'div.nrec',
            'URL': 'div.title > a'
        }
    }
    RE = {
        'url': re.compile(r'^https:\/\/(www\.)?ptt\.cc\/bbs\/[a-zA-Z0-9]+\/index[0-9]*\.html$')
    }

    def __init__(self, headers: dict):
        self.status = {
            'headers': headers,
        }
        self.soup = None

    def get(self, url: str, **headers: dict) -> t.Optional[Exception]:
        if not self.__check_url(url):
            raise Exception(f'Request url: {url} is not PTT board.')

        req = requests.get(url, headers = headers)
        self.__set_status(url, req)

        if not self.__sucess(req):
            raise Exception(f'Request to {url} is failed, response status is {req.status_code}')
        else:
            print(f'[INFO] {url} success')
    
    def __check_url(self, url: str) -> bool:
        if re.match(self.RE['url'], url):
            return True
        else:
            return False

    def __sucess(self, req: requests) -> bool:
        return req.status_code == 200

    def __set_status(self, url: str, req: requests) -> None:
        self.status['req_url'] = url
        self.status['res_code'] = req.status_code
        if self.__sucess(req):
            self.soup = BeautifulSoup(markup = req.text, features = 'html.parser')
        else:
            self.soup = None
            
    def prev_page(self) -> t.Optional[str]:
        prevElement = self.soup.select(self.SELECTOR.get("NAV_BUTTONS"))[1]
        if self.__is_disable(prevElement):
            return None
        else:
            return f'{self.BASE_URL}{prevElement["href"]}'

    def next_page(self) -> t.Optional[str]:
        nextElement = self.soup.select(self.SELECTOR.get("NAV_BUTTONS"))[2]
        if self.__is_disable(nextElement):
            return None
        else:
            return f'{self.BASE_URL}{prevElement["href"]}'

    def __is_disable(self, soup) -> bool:
        return 'disabled' in soup['class']

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

            postMetas.append(
                {
                    'url': post.select(self.SELECTOR.get("POST_META").get("DATE"))[0].text,
                    'author': post.select(self.SELECTOR.get("POST_META").get("AUTHOR"))[0].text,
                    'title': self.__regular_title(post.select(self.SELECTOR.get("POST_META").get("TITLE"))[0].text),
                    'date': self.__numerate_push(post.select(self.SELECTOR.get("POST_META").get("PUSH_NUMBER"))[0].text),
                    'pushNumber': f'{self.BASE_URL}{post.select(self.SELECTOR.get("POST_META").get("URL"))[0]["href"]}'
                }
                )

        return postMetas

    def __is_deleted(self, postSoup) -> bool:
        return postSoup.select('div.title > a') == []

    def __numerate_push(self, pushNumber: t.Union[str or int]) -> int:
        if pushNumber == '爆': return 100
        if pushNumber == '': return 0
        if pushNumber == 'XX': return -100
        if pushNumber[0] == 'X': return -(int(pushNumber[1]) * 10)
        return int(pushNumber)

    def __regular_title(self, title: str) -> str:
        return re.sub(r'[\/*?"<>|:"\s\n]', '', title)