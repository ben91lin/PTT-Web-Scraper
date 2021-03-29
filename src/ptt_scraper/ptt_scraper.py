import logger
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from './lib/pttData.py' import PttData
from './lib/pttPageViewer.py' import PttBoardViewer
from './config.py'  import config

class PTT:

    def __init__(self, config = config, PttData, PttPageViewer):
        self.config = config
        self.data = new PttData(self.config.get('boardName'))
        self.boardViewer = new PttBoardViewer()
        
    def getBoard(self):