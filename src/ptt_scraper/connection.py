import logging
import re
import requests
import typing as t
from bs4 import BeautifulSoup

class Connection():

    def __init__(self, headers: dict = None) -> None:
        self._original_headers = headers or None
        self._soup = None
        self._status = {
            'request_url': None,
            'headers': self._original_headers,
            'response_code': None,
            'looking_for': None,
        }

    def get(self, url: str, headers: t.Optional[dict] = None):
        self._reset_status()
        if not self._check_url(url): 
            raise Exception(f'This url is not a PTT link.')

        headers = headers if headers is not None else self._status['headers']
        request = requests.get(url, headers = headers)
        self._set_status(url, headers, request)

        if self._sucess(request):
            self._soup = BeautifulSoup(markup = request.text, features = 'html.parser')
            print(f'[INFO] {url} success')
        else:
            self.soup = None
            raise Exception(f'Request to {url} is failed, response status is {req.status_code}')

    def _reset_status(self) -> None:
        self._status['headers'] = self._original_headers
        self._status['request_url'] = None
        self._status['response_code'] = None
        self._status['looking_for'] = None

    def _check_url(self, url: str) -> bool:
        match = re.match(
            r'^https://(www\.)?ptt\.cc/bbs/[a-zA-Z0-9]+/(index[0-9]*\.html$|M\.[0-9]{10}\.A\.[A-Z0-9]{3}\.html$)',
            url
            )
        return True if match else False

    def _set_status(self, url: str, headers: dict, request: requests) -> None:
        self._status['request_url'] = url
        self._status['headers'] = headers
        self._status['response_code'] = request.status_code
        self._status['looking_for'] = self._parse_url(url)

    def _sucess(self, req: requests) -> bool:
        return req.status_code == 200

    def _parse_url(self, url: str) -> tuple:
        url = url.split('/')
        genre = 'board' if 'index' in url.pop() else 'article'
        board = url.pop()
        return board, genre

    def __repr__(self):
        return f'{self._status}'