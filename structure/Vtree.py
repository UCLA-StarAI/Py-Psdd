class Vtree(object):

    def __init__(self, idx, var=None, left=None, right=None):
        self._idx = idx
        self._var = var
        self._left = left
        self._right = right

    @property
    def idx(self):
        return self._idx

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, val):
        self._left = val

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, val):
        self._right = val

    @property
    def variables(self):
        if self._var:
            return [self._var]

        return (self._left.variables + self._right.variables)
