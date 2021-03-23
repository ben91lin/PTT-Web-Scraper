import logger
import requests
from bs4 import BeautifulSoup
from './abstract/boardViewer.py' import BoardViewer

class PttBoardViewer(BoardViewer):
    BaseUrl = 'https://www.ptt.cc'
    NavButtonsSelector = 'div.#action-bar-container div.btn-group-paging > a'
    PostsSelector = 'div.r-list-container div.r-ent'

    def __init__(self, url: str, headers: dict, BeautifulSoup = BeautifulSoup):
        self.soup = BeautifulSoup(markup = self._get(url, headers), features = 'html.parser')

    def _get(self, url: str, headers: dict):
        req = requests.get(url, headers = headers)

        if (req.status_code != 200):
            raise Exception(f'The request status is {req.status_code}')
        else:
            return req.text

    def prevPage(self) -> Union[None or str]:
        prevElement = self.soup.select(self.NavButtonsSelector)[1]
        if self._isDisable(prevElement):
            return None
        else:
            return f'{self.BaseUrl}{nextElement['href']}'

    def nextPage(self) -> Union[None or str]:
        nextElement = self.soup.select(self.NavButtonsSelector)[2]
        if self._isDisable(nextElement):
            return None
        else:
            return f'{self.BaseUrl}{prevElement['href']}'

    def _isDisable(self, linkSoup) -> bool:
        return 'disabled' in linkSoup['class']

    def oldestPage(self) -> str:
        return f'{self.BaseUrl}{self.soup.select(self.NavButtonsSelector)[0]['href']}'

    def newestPage(self) -> str:
        return f'{self.BaseUrl}{self.soup.select(self.NavButtonsSelector)[3]['href']}'

    def getPosts(self) -> list[dict]:
        posts = self.soup(self.PostsSelector)
        postMetas = []

        for post in posts:
            if (self._isDeleted(post)):
                continue
            
            pushNumber = self._numeratePush(post.select('div.nrec')[0].text)
            author = post.select('div.meta > div.author')[0].text
            date = post.select('div.meta > div.date')[0].text
            postTitle = self._regularTitle(post.select('div.title > a')[0].text)
            postUrl =  f'{self.Domain}{post.select('div.title > a')[0]['href']}'

            postMetas.append({'url': postUrl, 'author': author, 'title': postTitle, 'date': date, 'pushNumber': pushNum})
        return postMetas

    def _isDeleted(self, postSoup) -> bool:
        return postSoup.select('div.title > a') == []

    def _numeratePush(self, pushNumber: Union[str or int]) -> int:
        if pushNumber == '爆': return 100
        if pushNumber == '': return 0
        if pushNumber == 'XX': return -100
        if pushNumber[0] == 'X': return -(Int(pushNumber[0]) * 10)
        return pushNumber

    def _regularTitle(self, title: str) -> str:
        return re.sub('[\/*?"<>|:"\s\n]', '', title)