class Element(object):

    def __init__(self, prime, sub, parent):
        self._prime = prime
        self._sub = sub
        self._parent = parent

    @property
    def prime(self):
        return self._prime

    @property
    def sub(self):
        return self._sub

    @property
    def parent(self):
        return self._parent

