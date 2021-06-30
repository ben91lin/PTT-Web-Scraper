# import logging
# import re
# import time
import typing as t
from datetime import datetime
from time import sleep
from urllib.parse import urljoin

from board_viewer import PttBoardViewer
from article_viewer import PttArticleViewer
from datastructure import Data

class PTT:
    BASE_URL = 'https://www.ptt.cc'

    def __init__(
        self,
        headers: dict = {
            'cookie': 'over18=1;'
            },
        sleep: float = 1.0
        ):
        self.headers = headers
        self.sleep = sleep
        self.article_list = None
        
    def board(
        self,
        board_name: str,
        start: int,
        end: int = None
        ):
        if end is None:
            end = start + 1
        viewer = PttBoardViewer(self.headers)
        start_page = self.__start_page(viewer, start, board_name)
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        outputs = Data('Article list')

        if start_page is not None:
            current = start
            viewer.get(start_page)

            while viewer.has_prev_page() and (end == -1 or end > current):
                if start <= current:
                    outputs.data += self.update(viewer.articles(), now)
                current += 1
                viewer.get(viewer.prev_page())
                sleep(self.sleep)

        self.article_list = outputs
        return self.article_list

    def __start_page(
        self,
        viewer: 'PttBoardViewer',
        start: int,
        board_name: str
        ):
        if start == 0:
            return self.__board_url(board_name)

        viewer.get(self.__board_url(board_name))
        page_number = self.__page_number(viewer.prev_page())
        if page_number > start:
            return self.__board_url(board_name, str(page_number - start + 1))
        else:
            return None

    def __board_url(
        self,
        board_name: str,
        page_number: str = ''
        ) -> str:
        return urljoin(
            self.BASE_URL,
            '/'.join(
                [
                    'bbs',
                    board_name.capitalize(),
                    ''.join(
                        [
                            'index',
                            page_number,
                            '.html'
                        ]
                    )
                ]
            )
            )
    
    def __page_number(self, board_url: str) -> int:
        return int(board_url.split('index')[1].split('.html')[0])

    def update(
        self,
        target: t.Union[list, dict],
        time
        ) -> t.Union[list, dict]:
        assert isinstance(target, dict) or isinstance(target, list)
        if isinstance(target, dict):
            target['update'] = time
            return target 
        if isinstance(target, list):
            for t in target:
                self.update(t)

    def article(self):
        viewer = PttArticleViewer(self.headers)
        urls = [data['url'] for data in self.article_list.data]
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        outputs = list()

        for url in urls:
            outputs.data.append(
                self.update(viewer.get(url).article(), now)
            )
            sleep(self.sleep)

        return outputs