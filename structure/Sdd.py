import queue

class Sdd(object):

    def __init__(self, idx=0, lit=None, vtree=None):
        self._idx = idx
        self._lit = lit
        self._vtree = vtree

        if self._vtree is not None:
            self._vtree_idx = vtree.idx
        else:
            self._vtree_idx = None

        self._elements = []
        self._node_count = 1

    @property
    def is_terminal(self):
        return not self._elements

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, val):
        self.idx = val

    @property
    def lit(self):
        return self._lit

    @lit.setter
    def lit(self, val):
        self._lit = val

    def base(self):
        if self._lit is not None:
            return str(self._lit)

        res = ""
        for p, s in self._elements:
            if res != "":
                res += " OR "
            res += "(" + p.base() + " AND " + s.base() + ")"
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

    def copy(self):
        res = Sdd()
        for p, s in self._elements:
            res.add_element((p.copy(),s.copy()))
        res._idx = self._idx
        res._lit = self._lit
        res._vtree = self._vtree
        res._node_count = self._node_count
        return res

    def add_element(self, element):
        self._elements.append(element)

    def dump(self):
        res_cache = []

        Q = queue.Queue()
        vis = set()

        Q.put(self)
        vis.add(self._idx)

        while not Q.empty():
            u = Q.get()
            s = ''
            if u.is_terminal:
                if u._lit == 'T':
                    s = 'T {} {}'.format(u._idx, u._vtree.idx)
                if u._lit == 'F':
                    s = 'F {} {}'.format(u._idx, u._vtree.idx)
                if isinstance(u._lit, int):
                    s = 'L {} {} {}'.format(u._idx, u._vtree.idx, u._lit)
            else:
                s = 'D {} {} {}'.format(u._idx, u._vtree.idx, len(u._elements))
                for prime, sub in u._elements:
                    s += ' {} {}'.format(prime._idx, sub._idx)

                    if prime._idx not in vis:
                        Q.put(prime)
                        vis.add(prime._idx)
                    if sub._idx not in vis:
                        Q.put(sub)
                        vis.add(sub._idx)

            res_cache.insert(0, s)

        res = ''
        res += 'sdd {}\n'.format(self._node_count)
        for s in res_cache:
            res += s + '\n'

        return res