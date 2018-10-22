import math
import queue

from structure.Element import Element

PSDD_FILE_SPEC = \
'c ids of psdd nodes start at 0\n\
c psdd nodes appear bottom-up, children before parents\n\
c\n\
c file syntax:\n\
c psdd count-of-sdd-nodes\n\
c T id-of-trueNode-sdd-node id-of-vtree log(litProb)\n\
c F id-of-falseNode-sdd-node id-of-vtree\n\
c L id-of-literal-sdd-node id-of-vtree literal\n\
c D id-of-decomposition-sdd-node id-of-vtree number-of-elements {id-of-prime id-of-sub log(elementProb)}*\n\
c\n'

class Psdd(object):

    #num_nodes = 0

    def __init__(self, idx=None, vtree=None):
        # Please fix:
        #
        # Psdd.node_count += 1
        # self._index += Psdd.num_nodes
        #
        self._idx = idx
        self._vtree = vtree
        self._elements = []

        self._data = {}
        self._theta = None  # only not None if self.is_leaf
        self._weight = 0
        self._context_weight = 0

        self._num_parents = 0
        self._node_count = None

    @property
    def idx(self):
        return self._idx

    @property
    def is_leaf(self):
        return not self._elements

    @property
    def is_literal(self):
        return isinstance(self._base, int)

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
            for e in self._elements:
                p, s, theta = e.prime, e.sub, e.theta
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

    @property
    def node_count(self):
        return self._node_count

    @node_count.setter
    def node_count(self, value):
        self._node_count = value

    def add_element(self, element):
        self._elements.append(element)
        element.parent = self

    def set_element(self, i, e):
        self._elements[i] = e        
    
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

            for e in self._elements:
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

    def dump(self):
        res_cache = []

        Q = queue.Queue()
        vis = set()

        Q.put(self)
        vis.add(self._idx)

        while not Q.empty():
            u = Q.get()
            s = ''
            if u.is_leaf:
                if u._base == 'T':
                    s = 'T {} {} {}'.format(u._idx, u._vtree.idx, math.log(u._theta))
                if u._base == 'F':
                    s = 'F {} {}'.format(u._idx, u._vtree.idx)
                if isinstance(u._base, int):
                    s = 'L {} {} {}'.format(u._idx, u._vtree.idx, u._base)
            else:
                s = 'D {} {} {}'.format(u._idx, u._vtree.idx, len(u._elements))
                for e in u._elements:
                    s += ' {} {} {}'.format(e.prime._idx, e.sub._idx, math.log(e.theta))

                    if e.prime._idx not in vis:
                        Q.put(e.prime)
                        vis.add(e.prime._idx)
                    if e.sub._idx not in vis:
                        Q.put(e.sub)
                        vis.add(e.sub._idx)

            res_cache.insert(0, s)

        res = PSDD_FILE_SPEC
        res += 'psdd {}\n'.format(self._node_count)
        for s in res_cache:
            res += s + '\n'

        return res
