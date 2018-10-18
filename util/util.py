from structure.Vtree import *
from structure.Sdd import *
from structure.Psdd import *
from structure.Element import *

def vtree_from_file(vtree_file, return_node_cache=False):
    root = None
    node_cache = {}

    with open(vtree_file, 'r') as f:

        for line in f:
            line = line[:-1] #Get rid of the '\n' TODO

            head = line.split(' ')[0]

            if head == 'c':
                continue

            if head == 'vtree':
                continue

            tail = line.split(' ', 1)[1]

            if head == 'L':
                idx, var = [ int(x) for x in tail.split(' ') ]
                node_cache[idx] = Vtree(idx, var=var)

            if head == 'I':
                idx, left, right = [ int(x) for x in tail.split(' ') ]
                left = node_cache[left]
                right = node_cache[right]
                node_cache[idx] = Vtree(idx, left=left, right=right)

                root = node_cache[idx]

    if return_node_cache:
        return root, node_cache
    return root

def sdd_from_file(sdd_file, vtree_file):
    root = None
    node_cache = {}
    node_count = 0

    with open(sdd_file, "r") as f:

        for line in f:
            line = line[:-1] #Get rid of the '\n' TODO

            head = line.split(' ', 1)[0]

            if head == 'c':
                continue

            tail = line.split(' ', 1)[1]

            if head == 'sdd':
                node_count = int(tail)

            if head == 'F':
                idx = int(tail)
                root = node_cache[idx] = Sdd(idx, base="F")

            if head == 'T':
                idx = int(tail)
                root = node_cache[idx] = Sdd(idx, base="T")

            if head == 'L':
                idx, idx_vtree, lit = [ int(x) for x in tail.split(' ') ]
                root = node_cache[idx] = Sdd(idx, base=lit)

            if head == 'D':
                tmp = [ int(x) for x in tail.split(' ') ]
                idx, idx_vtree, ele_cnt = tmp[0], tmp[1], tmp[2]
                tmp = tmp[3:]
                u = Sdd(idx)
                for i in range(0, ele_cnt * 2, 2):
                    u.add_element((node_cache[tmp[i]], node_cache[tmp[i + 1]]))
                if idx == 1:
                    node_1 = u

                root = node_cache[idx] = u

    node_cache = {}

    root.vtree = vtree_from_file(vtree_file)

    root.node_count = root.normalize(root.node_count)

    return root

def psdd_from_file(psdd_file, vtree_file):
    root = None
    node_cache = {}
    node_count = 0

    vtree, vtree_node_cache = vtree_from_file(vtree_file, return_node_cache=True)

    with open(psdd_file, "r") as f:

        for line in f:
            line = line.strip([' ', '\n'])

            head = line.split(' ', 1)[0]

            if head == 'c':
                continue

            tail = line.split(' ', 1)[1]

            if head == 'psdd':
                node_count = int(tail)

            if head == 'T':
                idx, vtree_idx, log_prob = tail.split(' ')
                idx, vtree_idx, log_prob = int(idx), int(vtree_idx), float(log_prob)
                Psdd(vtree_node_cache[vtree_idx])

            if head == 'F':
                idx, vtree_idx = [ int(x) for x in tail.split(' ') ]

            if head == 'L':
                idx, vtree_idx, lit = [ int(x) for x in tail.split(' ') ]

            if head == 'D':
                tmp = [ int(x) for x in tail.split(' ') ]
                idx, vtree_idx, ele_cnt = tmp[0], tmp[1], tmp[2]
                tmp = tmp[3:]

def sdd_to_psdd(sdd):
    u = Psdd(sdd.idx, sdd.vtree)
    try:
        u._base = int(sdd.base)
    except:
        u._base = sdd.base

    for p, s in sdd.elements:
        u.add_element(Element(sdd_to_psdd(p), sdd_to_psdd(s)))
    u._node_count = sdd.node_count

    return u

def psdd_to_file(psdd, file_name):
    pass
