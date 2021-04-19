# PTT Web Scraper

Completely PTT Board Scraper.

Some datastructure in there.
* Board meta.

        {
            'url': ,
            'board': ,
            'download_datetime':
        }
        
* Simple article meta.

        {
            'url': ,
            'date': ,
            'author_id': ,
            'title': ,
            'push_number': ,
            'board': ,
            'download_datetime':
        }

* Detailed article meta.

        {
            'url': ,
            'datetime': ,
            'timestamp': ,
            'author_ip': ,
            'author_id': ,
            'author_nickname': ,
            'title': ,
            'content': ,
            'hrefs': ,
            'board': ,
            'download_datetime':
        }

* Comment meta.(Some comment doesn't have ip or time, depends on PTT board, )

        {
            'url': ,
            'datetime': ,
            'commentor_id': ,
            'commentor_ip': ,
            'tag': ,
            'content': ,
            'download_datetime':
        }