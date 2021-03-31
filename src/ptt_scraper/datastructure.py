import sys
import typing as t

class PttData:
    
    def __init__(self, boardName: str):
        self.boardName = boardName
        self.data = []

    def addPage(self, pageNumber: int, url: str):
        self.data.push(
            {
                'pageNumber': pageNumber,
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

class TupleStorage:
    __hash__ = None
    attributes: tuple[str] = ()

    def __init__(
        self, data: tuple
        ) -> None:
        self._tuple = data

    @classmethod
    def wrap(
        cls, new_attributes: tuple = (), name: t.Optional[str] = None
    ) -> t.Type["TupleStorage"]:

        class newcls(cls):
            attributes = cls.attributes + tuple(map(lambda attr: attr.lower(), new_attributes))

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

        newcls.__module__ = sys._getframe(1).f_globals["__name__"] # __main__
        name = f'{cls.__name__}-{name}' if name else cls.__name__
        newcls.__name__ = newcls.__qualname__ = name
        return newcls

    def __add__(self, other):
        # check if class exist.
        subclasses = TupleStorage.__subclasses__()
        target = self.__combine_name(self.__class__.__name__, other.__class__.__name__)
        if (self.__has_class(subclasses, target)):
            for sub in subclasses:
                if sub.__name__ == target:
                    return sub(data = (self._tuple + other._tuple))
        else:
            return TupleStorage.wrap(
                new_attributes = (self.attributes + other.attributes),
                name = target
                )(
                    data = (self._tuple + other._tuple)
                )

    def __combine_name(self, name1, name2):
        name1 = "".join(name1.split("-")[1:])
        name2 = "".join(name2.split("-")[1:])
        return f'{name1}+{name2}'

    def __has_class(self, subclasses, target):
        print(subclasses)
        names = tuple(map(lambda sub: sub.__name__, subclasses))
        if target in names:
            return True
        else:
            return False

    def __eq__(self, other):
        return other.__class__ is self.__class__ and other._tuple == self._tuple

    def __getitem__(self, key):
        if isinstance(key, str):
            if key.lower() not in self.__class__.attributes:
                raise KeyError(f'{key} is not in {self.__class__.name}.')
            else:
                return self._tuple[self.__class__.attributes.index(key.lower())]
        return self._tuple[key]

    def __iter__(self):
        # if object is iterable, it can use 'in' operator.
        return iter(self._tuple)

    def __len__(self):
        return len(self._tuple)

    def __repr__(self):
        return f'{self._tuple}'



