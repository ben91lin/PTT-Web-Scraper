import abc

class ArticleViewer(abc.ABC):

    @abc.abstractmethod
    def meta() -> dict:
        return NotImplemented

    @abc.abstractmethod
    def author() -> str:
        return NotImplemented

    @abc.abstractmethod
    def title() -> str:
        return NotImplemented

    @abc.abstractmethod
    def datetime() -> str:
        return NotImplemented

    @abc.abstractmethod
    def content() -> str:
        return NotImplemented

    @abc.abstractmethod
    def comments() -> list:
        return NotImplemented

    @abc.abstractmethod
    def medias() -> list:
        return NotImplemented