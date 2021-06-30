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

## Pipeline Operators

    $and, $all, # pass a list, if all condition is True, return True.
    $or, $in, # pass a list, if any condition is True, return True.
    $not, $not_in, # pass a list, if no condition is True, return True.
    $eq, $==,
    $ne, $!=,
    $gt, $>,
    $gte, $>=,
    $lt, $<,
    $lte, $<=

## Method & Output.

* board
    
    Browse ptt board and get 'article_list'.

        {
            'board': ,
            'url': ,
            'date': ,
            'author': ,
            'title': ,
            'push': ,
            'update':
        }

* article

        {
            'content': ,
            'meta': {
                'board': ,
                'url': ,
                'timestamp': ,
                'title': ,
                'push': ,
                'author': {
                    'ip': ,
                    'id': ,
                    'nickname':
                }
            },
            'comments: [
                {
                    'url': ,
                    'date': ,
                    'tag': ,
                    'content': ,
                    'commentor': {
                        'id': ,
                        'ip':
                    }
                }
            ],
            'href': {
                'article': ,
                'comments':
            },
            'update':
        }