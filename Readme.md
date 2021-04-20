# PTT Web Scraper

Completely PTT Board Scraper.

## Usage

    from ptt_scrpay import PTT

    ptt = PTT()
    ptt.board('board_name', start_page, end_page)
    ptt.simple_articles
    # filter data
    ptt.simple_articles.pipeline(
        { '$operator': (key, value) },
        { '$in': ('title', '爆掛') }
    )

Some datastructure in there.
        
* Simple articles.

        {
            'url': ,
            'date': ,
            'author_id': ,
            'title': ,
            'push_number': ,
            'board': ,
            'download_datetime':
        }

* Detailed articles.

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

* Comments.(Some comment doesn't have ip or time, depends on PTT board.)

        {
            'url': ,
            'datetime': ,
            'commentor_id': ,
            'commentor_ip': ,
            'tag': ,
            'content': ,
            'download_datetime':
        }