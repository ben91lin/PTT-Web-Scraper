import logging
import re
import requests
import typing as t
from bs4 import BeautifulSoup

class Connection():

    def __init__(self, headers: dict = None) -> None:
        self.__original_headers = headers or None
        self.__soup = None
        self.__status = {
            'request_url': None,
            'headers': self.__original_headers,
            'response_code': None,
            'looking_for': None,
        }

    def get(self, url: str, headers: t.Optional[dict] = None):
        self.__reset_status()
        if not self.__check_url(url): 
            raise Exception(f'This url is not a PTT link.')

        headers = headers if headers is not None else self.__status['headers']
        request = requests.get(url, headers = headers)
        self.__set_status(url, headers, request)

        if self.__sucess(request):
            self.__soup = BeautifulSoup(markup = request.text, features = 'html.parser')
            print(f'[INFO] {url} success')
        else:
            self.soup = None
            raise Exception(f'Request to {url} is failed, response status is {req.status_code}')

    def __reset_status(self) -> None:
        self.__status['headers'] = self.__original_headers
        self.__status['request_url'] = None
        self.__status['response_code'] = None
        self.__status['looking_for'] = None

    def __check_url(self, url: str) -> bool:
        match = re.match(
            r'^https://(www\.)?ptt\.cc/bbs/[a-zA-Z0-9]+/(index[0-9]*\.html$|M\.[0-9]{10}\.A\.[A-Z0-9]{3}\.html$)',
            url
            )
        return True if match else False

    def __set_status(self, url: str, headers: dict, request: requests) -> None:
        self.__status['request_url'] = url
        self.__status['headers'] = headers
        self.__status['response_code'] = request.status_code
        self.__status['looking_for'] = self.__parse_url(url)

    def __sucess(self, req: requests) -> bool:
        return req.status_code == 200

    def __parse_url(self, url: str) -> tuple:
        url = url.split('/')
        genre = 'board' if 'index' in url.pop() else 'article'
        board = url.pop()
        return board, genre

    def __repr__(self):
        return f'{self.__status}'