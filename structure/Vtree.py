class Vtree(object):

    def __init__(self, idx=-1, var=None, left=None, right=None):
        self._idx = idx
        self._var = var
        self._left = left
        self._right = right

        self._variable_list = None

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

    def variable_list(self):
        if self._var:
            return [self._var]
        if self._variable_list:
            return self._variable_list

        self._variable_list = self._left.variable_list + self._right.variable_list
        return self._variable_list
