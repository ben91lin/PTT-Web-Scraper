class PttData:
    
    def __init__(self, boardName: str):
        self.boardName = boardName
        self.data = []

    def addPage(self, pageNumber: int, url: str):
        self.data.push(
            {
                'pageNumber', pageNumber.
                'pageUrl': url,
                'posts': []
            }
        )
    
    def addPost(self, posts: property, url: str, title: str, date: str, author: str, pushNumber: int):
        posts.push(
            {
                'postUrl': url,
                'postTitle': title,
                'postDate': date,
                'postAuthor': author,
                'postPushNumber': pushNumber,
                'postContent': '',
                'postMedias': [],
                'pushMedias': [],
                'pushs':[]
            }
        )

    def addPostContent(self, postContent: property, html: str):
        postContent = html
    
    def addPostMedias(self, postMedias: property, url: str):
        postMedias.push(url)

    def addPushMedias(self, PushMedias: property, url: str):
        postMedias.push(url)

    def addPush(self, pushs: property, pushState: int, user: str, ip: str, datetime: str):
        pushs.push(pushState, user, ip, datetime)