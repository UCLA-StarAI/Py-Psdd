class Psdd(object):

    def __init__(self, sdd=None, data=None):
        self._idx = sdd.idx
        self._vtree = sdd.vtree
        self._base = sdd.base

        self._elements = []
        for p, s in sdd.elements:
            self._elements.append((Psdd(p), Psdd(s), None))

        self._data = {}
        self._theta = None

        if data is not None:
            for d, w in data:
                self.add_data(d, w)

    @property
    def is_leaf(self):
        return (not self._elements)

    @property
    def idx(self):
        return self._idx

    @property
    def base(self):
        return self._base

    @property
    def data(self):
        return self._data

    @property
    def weight(self):
        res = 0
        for d, w in self._data.items():
            res = res + w
        return res

    # optmization?
    def add_data(self, d, w):
        if not self._elements:

            if self._base == 'F':
                return False

            if self._base == 'T':
                if d not in self._data:
                    self._data[d] = w
                return True

            if isinstance(self._base, int):
                res = d[abs(self._base)]
                if self._base < 0:
                    res = not res

                if res:
                    self._data[d] = w

                return res

        for e in self._elements:
            if e[0].add_data(d, w):
                if e[1].add_data(d, w):
                    self._data[d] = w
                    return True
                else:
                    return False

        print("ERROR!")
        exit(1)

        return False

    def compute_parameter(self):
        for p, s in self._elements:
            p.weight
            s.weight
        pass
        # TODO