class Psdd(object):

    def __init__(self, sdd=None):
        self._idx = sdd.idx
        self._vtree = sdd.vtree
        self._base = sdd.base

        self._elements = []
        for p, s in sdd.elements:
            self._elements.append((Psdd(p), Psdd(s), None))

    @property
    def idx(self):
        return self._idx
    
    @property
    def base(self):
        return self._base


