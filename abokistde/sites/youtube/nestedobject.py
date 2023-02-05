"""
Easily filter and map big nested objects (dicts and lists). Works similar to JavaScript's Array.filter() and Array.map() methods.

Consider this example:

>>> cars = [
    { "manufacturer": "Audi", "models": [
        { "name": "A1", "year": 2010 },
        { "name": "A4", "year": 2013 }
    ]},
    { "manufacturer": "BMW", "models": [
        { "name": "X1", "year": 2011 },
        { "name": "X5", "year": 2014 }
    ]},
    { "manufacturer": "Mercedes", "models": [
        { "name": "C-class", "year": 2012 },
        { "name": "E-class", "year": 2015 }
    ]}
]

Assume we want to get the year of the X5. In standard Python, we would have to write something like this:

>>> [[car2['year'] for car2 in car['models'] if car2['name'] == 'X5'][0] for car in cars if car['manufacturer'] == 'BMW'][0]

With this class we can do the following:
>>> cars2 = NestedObject(cars)
>>> cars2.filter(lambda x: x['manufacturer'] == 'BMW')[0]['models'].filter(lambda x: x['name'] == 'X5')[0]['year']

or using the (unsafe) string index filter:
>>> cars2['_["manufacturer"] == "BMW"'][0]['models']['_["name"] == "X5"'][0]['year']
"""

class NestedObject:
    def __new__(self, data):
        if isinstance(data, dict):
            return NestedObjectDict(data)
        elif isinstance(data, list):
            return NestedObjectList(data)
        else:
            return data

class NestedObjectDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def __getitem__(self, key):
        if key in self: 
            return NestedObject(super().__getitem__(key))
        else:
            return None

class NestedObjectList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__list__ = self

    def filter(self, func):
        return NestedObjectList(list(filter(func, self)))

    def _filterStr(self, expr):
        fun = lambda _: eval(expr)
        return self.filter(fun)

    def map(self, func):
        return NestedObjectList(list(map(func, self)))

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return NestedObjectList(super().__getitem__(idx))
        elif isinstance(idx, str):
            return self._filterStr(idx)
        elif callable(idx):
            return self.filter(idx)
        elif idx < len(self):
            return NestedObject(super().__getitem__(idx))
        else:
            return None