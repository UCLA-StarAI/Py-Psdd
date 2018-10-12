from structure.Element import Element

PSDD_FILE_SPEC = \
    'c ids of psdd nodes start at 0\n\
    c psdd nodes appear bottom-up, children before parents\n\
    c\n\
    c file syntax:\n\
    c psdd count-of-sdd-nodes\n\
    c L id-of-literal-sdd-node id-of-vtree literal\n\
    c T id-of-trueNode-sdd-node id-of-vtree log(litProb)\n\
    c F id-of-falseNode-sdd-node id-of-vtree\n\
    c D id-of-decomposition-sdd-node id-of-vtree number-of-elements {id-of-prime id-of-sub log(elementProb)}*\n\
    c\n'


class Psdd(object):

    def __init__(self, vtree, sdd=None, data={}):

        self._vtree = vtree

        self._data = {}

        self._theta = None  # only not None if self.is_leaf

        self._weight = 0
        self._context_weight = 0

        self._num_parents = 0

        if sdd is None:
            self._idx = 0
            self._base = 'T'
        else:
            self._vtree_idx = sdd.vtree_idx
            try:
                self._base = int(sdd.base)
            except:
                self._base = sdd.base

            self._elements = []
            for p, s in sdd.elements:
                self.add_element(Element(Psdd(p.vtree, p), Psdd(s.vtree, s)))

        if data is not None:
            for d, w in data.items():
                self.add_data(d, w)

    @property
    def idx(self):
        return self._idx

    @property
    def is_leaf(self):
        return (not self._elements)

    @property
    def base(self):
        return self._base

    @property
    def vtree(self):
        return self._vtree

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        if data is not None:
            self.data = None
            for d, w in data.items():
                self.add_data(d, w)

        if data is None:
            self._weight = 0
            for e, theta in self._elements:
                p, s = e.prime, e.sub
                p._context_weight = s._context_weight = 0
                p.data = s.data = None

    @property
    def weight(self):
        return self._weight

    @property
    def context_weight(self):
        return self._context_weight

    @property
    def num_parents(self):
        return self._num_parents

    @num_parents.setter
    def num_parents(self, value):
        self._num_parents = value

    def add_element(self, element):
        self._elements.append((element, None))
        element.parent = self

    def remove_element(self, index_in_elements):
        self._elements[index_in_elements].parent = None
        del self._elements[index_in_elements]

    # optmization?
    def add_data(self, asgn, w):
        # if example is already added to the psdd
        if asgn in self._data:
            return True

        self._context_weight = self._context_weight + w

        if self.is_leaf:

            if self._base == 'F':
                return False

            if self._base == 'T':
                self._data[asgn] = w

                # get the variable from the vtree leaf
                v = None
                for x in self._vtree.variables:
                    v = x                
                
                if asgn[v]:
                    self._weight = self._weight + w

                return True

            if isinstance(self._base, int):
                res = asgn[abs(self._base)]
                if self._base < 0:
                    res = not res

                if res:
                    self._data[asgn] = w

                return res

        else:

            for e, theta in self._elements:
                if e.prime.add_data(asgn, w):
                    if e.sub.add_data(asgn, w):
                        self._data[asgn] = w
                        self._weight = self._weight + w
                        return True
                    else:
                        return False

        print('ERROR!')
        print(asgn)

        return False

    def calculate_parameter(self):
        for i, e in enumerate(self._elements):
            e, theta = e
            p, s = e.prime, e.sub
            theta = (p._weight + 1.0) / (p._context_weight + float(len(self._elements)))
            self._elements[i] = (e, theta)

            p.calculate_parameter()
            s.calculate_parameter()

        if self.is_leaf:
            self._theta = (self._weight + 1.0) / (self._context_weight + 1.0)

    def dump(self):
        if self.is_leaf:
            pass
        else:
            pass
