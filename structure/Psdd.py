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

    def __init__(self, idx=None, vtree=None):
        self._idx = idx
        self._lit = None
        self._vtree = vtree
        self._elements = []

        # self._data = {}
        self._theta = 0.0  # only used for terminal nodes
        self._weight = 0.0 # only used for terminal nodes
        self._context_weight = 0.0

        self._num_parents = 0
        self._node_count = None

    @property
    def idx(self):
        return self._idx

    @property
    def is_terminal(self):
        return not self._elements

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
                f = {}
                g = set()
                self.add_data(d, w, f, g, True)

        if data is None:
            self._weight = 0
            self._data = {}
            for e in self._elements:
                p, s, theta = e.prime, e.sub, e.theta
                p._context_weight = s._context_weight = 0
                p.data = None
                s.data = None

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
                    s = 'T {} {} {}'.format(u._idx, u._vtree.idx, u._theta)
                if u._lit == 'F':
                    s = 'F {} {}'.format(u._idx, u._vtree.idx)
                if isinstance(u._lit, int):
                    s = 'L {} {} {}'.format(u._idx, u._vtree.idx, u._lit)
            else:
                s = 'D {} {} {}'.format(u._idx, u._vtree.idx, len(u._elements))
                for e in u._elements:
                    s += ' {} {} {}'.format(e.prime._idx, e.sub._idx, e.theta)

                    if e.prime._idx not in vis:
                        Q.put(e.prime)
                        vis.add(e.prime._idx)
                    if e.sub._idx not in vis:
                        Q.put(e.sub)
                        vis.add(e.sub._idx)

            # if s == '':
            #     print('s: ', s)
            #     print('idx: ', u._idx)
            #     print('base: ', u._base)
            #     print('vtree_idx: ', u._vtree.idx)
            #     print('element_cnt: ', len(u._elements))
            #     print('is_terminal: ', u.is_terminal)
            res_cache.insert(0, s)

        res = PSDD_FILE_SPEC
        res += 'psdd {}\n'.format(self._node_count)
        for s in res_cache:
            res += s + '\n'

        return res
