import sys
import typing as t

class Data:
    '''
        Use list comprehension instead of filter(), it's faster and more clearly.
    '''

    def __init__(self, name: str = '', data: list = None):
        self._name = name
        self._data = data or []
        self._OPERATOR = {
            '$and': self.all,
            '$all': self.all,
            '$or': self.contain,
            '$in': self.contain,
            '$not': self.not_contain,
            '$not_in': self.not_contain,
            '$eq': self.equal,
            '$==': self.equal,
            '$ne': self.not_equal,
            '$!=': self.not_equal,
            '$gt': self.greater,
            '$>': self.greater,
            '$gte': self.greater_and_equal,
            '$>=': self.greater_and_equal,
            '$lt': self.less,
            '$<': self.less,
            '$lte': self.less_and_equal,
            '$<=': self.less_and_equal,
            }
        

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, d):
            self._data = d

    def pipeline(self, *args):
        '''
        { "$operator": (key, value) }, { "$operator": (key, value) }
        '''
        for arg in args:
            for k, v in arg.items():
                self._OPERATOR[k](v[0], v[1])

    def filter(self, cb):
        self._data = filter(cb, self._data)
        return self

    def all(self, key: str, values: t.Union[str, list, tuple]) -> 'Data':
        values = [values] if isinstance(values, str) else values
        self._data = [data for data in self._data if all(v in data.get(key, '') for v in values)]
        return self

    def contain(self, key: str, values: t.Union[str, list, tuple]) -> 'Data':
        values = [values] if isinstance(values, str) else values
        self._data = [data for data in self._data if any(v in data.get(key, '') for v in values)]
        return self

    def not_contain(self, key: str, values: t.Union[str, list, tuple]) -> 'Data':
        values = [values] if isinstance(values, str) else values
        self._data = [data for data in self._data if any(v not in data.get(key, '') for v in values)]
        return self

    def equal(self, key: str, value) -> 'Data':
        self._data = [data for data in self._data if data.get(key, '') == value]
        return self

    def not_equal(self, key: str, value) -> 'Data':
        self._data = [data for data in self._data if data.get(key, '') != value]
        return self

    def greater(self, key: str, value) -> 'Data':
        self._data = [data for data in self._data if data.get(key, '') > value]
        return self

    def greater_and_equal(self, key: str, value) -> 'Data':
        self._data = [data for data in self._data if data.get(key, '') >= value]
        return self

    def less(self, key: str, value) -> 'Data':
        self._data = [data for data in self._data if data.get(key, '') < value]
        return self

    def less_and_equal(self, key: str, value) -> 'Data':
        self._data = [data for data in self._data if data.get(key, '') <= value]
        return self

    def __repr__(self):
        if len(self._data) == 0:
            return f'{self._name}: It\'s empty.'
        else:
            return f'{self._name}: lens({len(self._data)}), {self._data[0].keys()}, size({sys.getsizeof(self._data)}bytes).'