# PTT Web Scraper

Completely PTT Board Scraper.

## Usage

    from ptt_scrpay import PTT

    ptt = PTT()
    # get article list.
    ptt.board('board_name', start_page, end_page)
    # filter data.
    ptt.article_list.pipeline(
        { '$operator': (key, value) },
        { '$in': ('title', '爆掛') },
        ...
    )
    # get articles.
    articles = ptt.article()
    # get article meta only.
    metas = ptt.meta()
    # get comment only.
    comments = ptt.comment()

## Pipeline Operators

$all, $in, $not_in, $equal, $==, $not_equal, $!=, $greater, $>, $greater_and_equal, $>=, $less, $<, $less_and_equal, $<=

## Method & Output.

* board
    
    Browse ptt board and get 'article_list'.

        {
            'url': ,
            'date': ,
            'author_id': ,
            'title': ,
            'push_number': ,
            'board': ,
            'download_time':
        }

* article

        {
            'url': ,
            'datetime': ,
            'timestamp': ,
            'author_ip': ,
            'author_id': ,
            'author_nickname': ,
            'title': ,
            'push_number': ,
            'content': ,
            'comments: ,
            'href_in_article': ,
            'href_in_comments: ,
            'board': ,
            'download_time':
        }

* meta

        {
            'url': ,
            'datetime': ,
            'timestamp': ,
            'author_ip': ,
            'author_id': ,
            'author_nickname': ,
            'title': ,
            'push_number': ,
            'download_time':
        }

* comment
    
    Comment only, but some comment doesn't have ip or time, depends on  board.

        {
            'url': ,
            'datetime': ,
            'commentor_id': ,
            'commentor_ip': ,
            'tag': ,
            'content': ,
            'download_time':
        }

* href_in_article

        {
            'url': ,
            'href_in_article': ,
            'download_time':
        }

* href_in_comment

        {
            'url': ,
            'href_in_comment': ,
            'download_time':
        }