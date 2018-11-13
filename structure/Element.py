class Element(object):

    def __init__(self, prime, sub, theta=None, parent=None):
        self._prime = prime
        self._sub = sub
        self._weight = 0.0
        self._prime.num_parents += 1
        self._sub.num_parents += 1
        self._theta = theta
        self._parent = parent
        self._splittable_variables = set()

    @property
    def prime(self):
        return self._prime

    @prime.setter
    def prime(self, value):
        if self._prime is not None:
            self._prime.numParents -= 1
        self._prime = value
        self._prime.numParents += 1

    @property
    def sub(self):
        return self._sub

    @sub.setter
    def sub(self, value):
        if self._sub is not None:
            self._sub.numParents -= 1
        self._sub = value
        self._sub.numParents += 1

    @property
    def weight(self):
        return self.weight

    @weight.setter
    def weight(self, val):
        self._weight = val

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def theta(self):
        return self._theta

    @theta.setter
    def theta(self, value):
        self._theta = value

    @property
    def splittable_variables(self):
        return self._splittable_variables

    @splittable_variables.setter
    def splittable_varialbes(self, value):
        self._splittable_variables = value

    def remove_splittable_varialbe(self, variable_to_remove):
        self._splittable_variables.discard(variable_to_remove)
