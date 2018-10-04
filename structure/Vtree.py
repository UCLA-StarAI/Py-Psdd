class Vtree(object):
    
    def __init__(self, idx=-1, var=None, left=None, right=None):
        self._idx = idx
        self._var = var
        self._left = left
        self._right = right

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

    def get_variable_set():
        pass
