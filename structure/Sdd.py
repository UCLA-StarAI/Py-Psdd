class Sdd(object):

    def __init__(self, idx, base=None, vtree=None,):
        self._idx = idx
        self._base = base
        self._elements = []
        self._node_count = 1

        if vtree is None:
            self._vtree = None
            self._vtree_idx = None
        else:
            self._vtree = vtree
            self._vtree_idx = vtree.idx

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
    def node_count(self):
        return self._node_count

    @node_count.setter
    def node_count(self, val):
        self._node_count = val

    @property
    def vtree_idx(self):
        return self._vtree_idx

    @vtree_idx.setter
    def vtree_idx(self, idx):
        self._vtree_idx = idx

    @property
    def vtree(self):
        return self._vtree

    @vtree.setter
    def vtree(self, u):
        self._vtree = u
        self._vtree_idx = u.idx
        for p, s in self._elements:
            p.vtree = u.left
            s.vtree = u.right

    def normalize(self, next_idx):
        for e in self._elements:
            for u in e:

                uv = u.vtree
                if not uv.is_leaf:

                    if u.is_leaf:
                        if u._base == 'T':
                            u._base = None
                            u.add_element((Sdd(next_idx, 'T', uv.left), Sdd(next_idx + 1, 'T', uv.right)))
                            next_idx += 2

                        if u._base == 'F':
                            u._base = None
                            u.add_element((Sdd(next_idx, 'T', uv.left), Sdd(next_idx + 1, 'F', uv.right)))
                            next_idx += 2

                        if isinstance(u._base, int):
                            var = u._base
                            u._base = None

                            if var in uv.left.variables:
                                u.add_element((Sdd(next_idx, var, uv.left), Sdd(next_idx + 1, 'T', uv.right)))
                                next_idx += 2
                                u.add_element((Sdd(next_idx, -var, uv.left), Sdd(next_idx + 1, 'F', uv.right)))
                                next_idx += 2

                            if var in uv.right.variables:
                                u.add_element((Sdd(next_idx, 'T', uv.left), Sdd(next_idx + 1, var, uv.right)))
                                next_idx += 2

                    next_idx = u.normalize(next_idx)
                    
        return next_idx

    def add_element(self, element):
        self._elements.append(element)