class Sdd(object):

    def __init__(self, idx=-1, base=None):
        self._idx = idx
        self._base = base
        self._elements = []
        self._vtree = None

    def is_leaf(self):
        return (not self._elements)

    @property
    def idx(self):
        return self._idx

    @property
    def base(self):
        if self._base is not None:
            return str(self._base)

        res = ""
        for p, s in self._elements:
            if res != "":
                res += " OR "
            res += "(" + p.base + " AND " + s.base + ")"
            res = "(" + res + ")"

        return res

    @property
    def elements(self):
        return self._elements

    @property
    def vtree(self):
        return self._vtree

    @vtree.setter
    def vtree(self, u):        
        self._vtree = u        
        for p, s in self._elements:
            p.vtree = u.left
            s.vtree = u.right

    def add_element(self, element):
        self._elements.append(element)