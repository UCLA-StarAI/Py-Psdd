class Vtree(object):

    def __init__(self, idx, var=None, left=None, right=None, parent=None):
        self._idx = idx
        self._var = var
        self._left = left
        self._right = right
        self._parent = parent

        if self._var is not None:
            self._var_set = set([self._var])
        else:
            self._var_set = None

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
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, val):
        self._parent = val

    @property
    def is_terminal(self):
        return self._var is not None

    @property
    def variables(self):
        if self._var_set is not None:
            return self._var_set

        self._var_set = self._left.variables | self._right.variables
        
        return self._var_set
