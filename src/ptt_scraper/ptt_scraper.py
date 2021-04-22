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
        self.article_list = None
        
    def board(
        self,
        board_name: str,
        start_page: int,
        end_page: int = None
        ):
        if end_page is None:
            end_page = start_page
        viewer = PttBoardViewer(self.headers).get(self.__board_url(board_name))
        outputs = Data('Article list')

        current_page = 0
        while end_page >= current_page and viewer.has_prev_page():
            if start_page <= current_page: 
                outputs.data += viewer.articles()
            viewer.get(viewer.prev_page())
            current_page += 1
            sleep(self.sleep)

        self.article_list = outputs
        return self.article_list

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

    def meta(self):
        viewer = PttArticleViewer(self.headers)
        urls = [data['url'] for data in self.article_list.data]
        outputs = Data('Metas')

        for url in urls:
            outputs.data.append(
                viewer.get(url).meta()
            )
            sleep(self.sleep)

        return outputs

    def article(self):
        viewer = PttArticleViewer(self.headers)
        urls = [data['url'] for data in self.article_list.data]
        outputs = Data('Articles')

        for url in urls:
            outputs.data.append(
                viewer.get(url).article()
            )
            sleep(self.sleep)

        return outputs

    def comment(self):
        viewer = PttArticleViewer(self.headers)
        outputs = Data('Comments')
        urls = [data['url'] for data in self.article_list.data]

        for url in urls:
            comments = viewer.get(url).comments()
            for c in comments:
                c['url'] = url
            outputs.data += comments
            sleep(self.sleep)

        return outputs

    def href_in_article(self):
        viewer = PttArticleViewer(self.headers)
        outputs = Data('Href in Article')
        urls = [data['url'] for data in self.article_list.data]

        for url in urls:
            outputs.data.append(
                {
                    'url': url,
                    'href_in_article': viewer.get(url).href_in_article()
                }
            )
            sleep(self.sleep)

        return outputs

    def href_in_comment(self):
        viewer = PttArticleViewer(self.headers)
        outputs = Data('Href in Comment')
        urls = [data['url'] for data in self.article_list.data]

        for url in urls:
            outputs.data.append(
                {
                    'url': url,
                    'href_in_comment': viewer.get(url).href_in_comment()
                }
            )
            sleep(self.sleep)

        return outputs
