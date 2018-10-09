class Element(object):

    def __init__(self, prime, sub, parent=None):
        self._prime = prime
        self._sub = sub
        self._parent = parent
        self._splittable_variables = set()

    @property
    def prime(self):
        return self._prime

    @prime.setter
    def prime(self, value):
        self._prime = value

    @property
    def sub(self):
        return self._sub

    @sub.setter
    def sub(self, value):
        self._sub = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def splittable_variables(self):
        return self._splittable_variables

    @splittable_variables.setter
    def splittable_varialbes(self, value):
        self._splittable_variables = value

    def remove_splittable_varialbe(self, variable_to_remove):
        self._splittable_variables.discard(variable_to_remove)
