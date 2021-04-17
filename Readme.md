# PTT Web Scraper

Completely PTT Board Scraper.

Some datastructure in there.
* simple article meta.
    {
        'url': ,
        'date': ,
        'author_id': ,
        'title': ,
        'push_number': ,
        'scrape_timestamp':
    }
* detailed article meta.
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
        'scrape_timestamp':
    }
* comment meta.
Depend PTT board, some comment doesn't have ip/time.
    {
        'url': ,
        'datetime': ,
        'commentor_id': ,
        'commentor_ip': ,
        'tag': ,
        'content': ,
        'scrape_timestamp':
    }