from structure.Vtree import *
from structure.Sdd import *
from structure.Psdd import *
from structure.Element import *
from algo import algo

def cnf_from_file(cnf_file):
    cnf = []
    with open(cnf_file, 'r') as f:
        for line in f:
            line = line[:-1]
            if line[0] == 'c':
                continue
            elif line[0] == 'p':
                var_num = int(line.split(' ')[2])
            else:
                cnf.append([int(x) for x in line.split(' ')][:-1])
    return cnf

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
                u = Vtree(idx, left=left, right=right)
                left.parent = u
                right.parent = u
                node_cache[idx] = u

                root = node_cache[idx]

    if return_node_cache:
        return root, node_cache
    return root

def sdd_from_file(sdd_file, vtree_file):
    root = None
    node_cache = {}
    node_count = 0

    vtree, vtree_node_cache = vtree_from_file(vtree_file, True)

    with open(sdd_file, "r") as f:

        for line in f:
            line = line[:-1]

            head = line.split(' ', 1)[0]

            if head == 'c':
                continue

            tail = line.split(' ', 1)[1]

            if head == 'sdd':
                node_count = int(tail)

            idx = None
            if head == 'F':
                idx = int(tail)
                node_cache[idx] = Sdd(idx, 'F')

            if head == 'T':
                idx = int(tail)
                node_cache[idx] = Sdd(idx, 'T')

            if head == 'L':
                idx, vtree_idx, lit = [ int(x) for x in tail.split(' ') ]
                u = Sdd(idx, lit, vtree_node_cache[vtree_idx])
                node_cache[idx] = u

            if head == 'D':
                tmp = [ int(x) for x in tail.split(' ') ]
                idx, vtree_idx, ele_cnt = tmp[0], tmp[1], tmp[2]
                tmp = tmp[3:]

                u = Sdd(idx, None, vtree_node_cache[vtree_idx])
                for i in range(0, ele_cnt * 2, 2):
                    u.add_element((node_cache[tmp[i]], node_cache[tmp[i + 1]]))

                node_cache[idx] = u
            if idx is not None:
                root = node_cache[idx]

    node_cache = {}

    root.node_count = node_count

    return root

def sdd_to_psdd(sdd):
    u = Psdd(sdd.idx, sdd.vtree)
    u._lit = sdd._lit

    for p, s in sdd.elements:
        u.add_element(Element(sdd_to_psdd(p), sdd_to_psdd(s)))
    u._node_count = sdd.node_count

    return u

def psdd_from_vtree(vtree_file):
    vtree = vtree_from_file(vtree_file)

    root = Sdd(0, 'T', vtree)
    root = algo.normalize(root, vtree)
    root.node_count = algo.re_index(root)

    return sdd_to_psdd(root)

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

def psdd_to_file(psdd, file_name):
    with open(file_name, 'w') as f:
        f.write(psdd.dump())
