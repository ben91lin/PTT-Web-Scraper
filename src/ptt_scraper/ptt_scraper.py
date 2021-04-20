import logging
import re
import time
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
        self.simple_articles = Data('Simple article meta')
        self.detailed_articles = Data('Detailed article meta')
        self.comments = Data('Comments meta')
        
    def board(
        self,
        board_name: str,
        start: int,
        end: int = None
        ):
        end = start if end is None else end
        viewer = PttBoardViewer(self.headers)
        current = 0
        outputs = []

        viewer.get(self.__board_url(board_name))
        while end >= current and viewer.has_prev_page():
            if start <= current: 
                outputs += viewer.articles()
            viewer.get(viewer.prev_page())
            current += 1
            sleep(self.sleep)

        self.simple_articles.data = outputs
        return self.simple_articles

    def __board_url(self, board_name):
        return urljoin(
            self.BASE_URL,
            '/'.join(
                [
                    'bbs',
                    board_name.capitalize(),
                    'index.html'
                ]
            )
            )

    def articles(self, comments: bool = True):
        viewer = PttArticleViewer(self.headers)
        outputs = []
