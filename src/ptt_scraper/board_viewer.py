import logging
import re
import requests
import typing as t
from bs4 import BeautifulSoup
from abstract.board_viewer import BoardViewer

class PttBoardViewer(BoardViewer):
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
    RE = {
        'url': re.compile(r'^https://(www\.)?ptt\.cc/bbs/[a-zA-Z0-9]+/index[0-9]*\.html$')
    }

    def __init__(self, headers: dict):
        self.status = {
            'headers': headers,
            'board': None,
            'req_url': None,
`           'res_code': None
        }
        self.soup = None

    def get(self, url: str, headers: t.Optional[dict] = None) -> t.Optional[Exception]:
        if not self.__check_url(url):
            raise Exception(f'Request url: {url} is not a PTT board link.')
        
        headers = headers or self.status.get('headers')
        req = requests.get(url, headers = headers)
        self.__set_status(url, req)

        if self.__sucess(req):
            self.soup = BeautifulSoup(markup = req.text, features = 'html.parser')
            print(f'[INFO] {url} success')
        else:
            self.soup = None
            raise Exception(f'Request to {url} is failed, response status is {req.status_code}')
    
    def __check_url(self, url: str) -> bool:
        if re.match(self.RE['url'], url):
            return True
        else:
            return False

    def __sucess(self, req: requests) -> bool:
        return req.status_code == 200

    def __set_status(self, url: str, req: requests) -> None:
        self.status['board'] = url.split('bbs/')[1].split('/')[0]
        self.status['req_url'] = url
        self.status['res_code'] = req.status_code
            
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
            return f'{self.BASE_URL}{nextElement["href"]}'

    def __is_disable(self, soup) -> bool:
        return 'disabled' in soup['class']

    def oldest_page(self) -> str:
        return f'{self.BASE_URL}{self.soup.select(self.SELECTOR.get("NAV_BUTTONS"))[0]["href"]}'

    def newest_page(self) -> str:
        return f'{self.BASE_URL}{self.soup.select(self.SELECTOR.get("NAV_BUTTONS"))[3]["href"]}'

    def articles(self) -> list[dict]:
        selections = self.soup.select(self.SELECTOR.get('ARTICLES'))
        outputs = []

        for article in selections:
            if (self.__is_deleted(article)):
                continue

            outputs.append(
                {
                    'board': self.status['board'],
                    'url': article.select(self.SELECTOR.get("ARTICLE_META").get("DATE"))[0].text,
                    'author': article.select(self.SELECTOR.get("ARTICLE_META").get("AUTHOR"))[0].text,
                    'title': self.__regular_title(article.select(self.SELECTOR.get("ARTICLE_META").get("TITLE"))[0].text),
                    'date': self.__numerate_push(article.select(self.SELECTOR.get("ARTICLE_META").get("PUSH_NUMBER"))[0].text),
                    'pushNumber': f'{self.BASE_URL}{article.select(self.SELECTOR.get("ARTICLE_META").get("URL"))[0]["href"]}'
                }
                )

        return outputs

    def __is_deleted(self, soup) -> bool:
        return soup.select('div.title > a') == []

    def __numerate_push(self, pushNumber: t.Union[str or int]) -> int:
        if pushNumber == '爆': return 100
        if pushNumber == '': return 0
        if pushNumber == 'XX': return -100
        if pushNumber[0] == 'X': return -(int(pushNumber[1]) * 10)
        return int(pushNumber)

    def __regular_title(self, title: str) -> str:
        return re.sub(r'[\/*?"<>|:"\s\n]', '', title)

    def __repr__(self) -> str:
        return f'{self.status}'