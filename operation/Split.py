class Split(Primitive):

    def __init__(self, element_to_split, variable_to_split, depth):
        self._element_to_split = element_to_split
        self._variable_to_split = variable_to_split
        self._depth = depth

    @property
    def element_to_split(self):
        return self._element_to_split

    @property
    def variable_to_split(self):
        return self._variable_to_split

    @property
    def depth(self):
        return self._depth

    def execute(self):
        raise NotImplementedError()

    def simulate(self):
        raise NotImplementedError()
