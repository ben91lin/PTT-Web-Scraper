# PTT Web Scraper

Completely PTT Board Scraper.

Some datastructure in there.
* Board meta.

        {
            'url': ,
            'board': ,
            'scrape_datetime':
        }

* Simple article meta.

        {
            'url': ,
            'date': ,
            'author_id': ,
            'title': ,
            'push_number': ,
            'board': ,
            'scrape_datetime':
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
            'scrape_datetime':
        }
* Comment meta.(Depend PTT board, some comment doesn't have ip/time.)

        {
            'url': ,
            'datetime': ,
            'commentor_id': ,
            'commentor_ip': ,
            'tag': ,
            'content': ,
            'scrape_datetime':
        }