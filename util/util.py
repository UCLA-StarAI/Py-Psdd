from structure.Vtree import *
from structure.Sdd import *
from structure.Psdd import *

def vtree_from_file(vtree_file):
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

    node_cache = {}

    return root

def sdd_from_file(sdd_file, vtree_file):
    root = None
    node_cache = {}

    with open(sdd_file, "r") as f:

        for line in f:
            line = line[:-1] #Get rid of the '\n' TODO

            head = line.split(' ')[0]

            if head == 'c':
                continue

            if head == 'sdd':
                continue

            tail = line.split(' ', 1)[1]

            if head == 'F':
                idx = int(tail)
                root = node_cache[idx] = Sdd(idx, base="F")

            if head == 'T':
                idx = int(tail)
                root = node_cache[idx] = Sdd(idx, base="T")

            if head == 'L':
                idx, idx_vtree, lit = [ int(x) for x in tail.split(' ') ]
                root = node_cache[idx] = Sdd(idx=idx, base=lit)

            if head == 'D':
                tmp = [ int(x) for x in tail.split(' ') ]
                idx, idx_vtree, ele_cnt = tmp[0], tmp[1], tmp[2]
                tmp = tmp[3:]
                u = Sdd(idx)
                for i in range(0, ele_cnt * 2, 2):
                    u.add_element((node_cache[tmp[i]], node_cache[tmp[i + 1]]))

                root = node_cache[idx] = u

    node_cache = {}

    root.vtree = vtree_from_file(vtree_file)

    return root

def sdd_to_psdd(sdd):
    return Psdd(sdd)