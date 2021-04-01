import abc

class BoardViewer(abc.ABC):

    @abc.abstractmethod
    def get() -> None:
        # Get HTML doc. Storage in property.
        return NotImplemented

    @abc.abstractmethod
    def prev_page() -> str:
        # Return PrevPage link.
        return NotImplemented

    @abc.abstractmethod
    def next_page() -> str:
        # Return nextPage link.
        return NotImplemented

    @abc.abstractmethod
    def oldest_page(self) -> str:
        # Return oldestPage link.
        return NotImplemented

    @abc.abstractmethod
    def newest_page(self) -> str:
        # Return newestPage link.
        return NotImplemented

    @abc.abstractmethod
    def get_posts() -> list:
        # Return postMetas.
        # Include post url, author, date, pushNum .etc
        return NotImplemented