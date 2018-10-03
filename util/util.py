from structure.Vtree import *

def vtree_from_file(vtree_file):
    root = None
    node_cache = {}

    with open(vtree_file, 'r') as f:

        for line in f:
            line = line[:-1] #TODO            

            head, tail = line.split(' ', 1)

            if head == 'c':
                continue

            if head == 'vtree':
                continue

            if head == 'L':
                idx, var = [ int(x) for x in tail.split(' ') ]
                node_cache[idx] = Vtree(idx, var=var)

            if head == 'I':
                idx, left, right = [ int(x) for x in tail.split(' ') ]
                left = node_cache[left]
                right = node_cache[right]
                node_cache[idx] = Vtree(idx, left=left, right=right)

    root = node_cache[0]
    node_cache = {}

    return root

def sdd_from_file(sdd_file, vtree_file):
    root = None
    node_cache = {}
    vtree = vtree_from_file(vtree_file)

    with open(sdd_file, "r") as f:

        for line in f:

            head, tail = line.split(' ', 1)

            if head == 'c':
                continue

            if head == 'sdd':
                continue

            if head == 'F':
                pass

            if head == 'T':
                pass

            if head == 'L':
                pass

            if head == 'D':
                pass


def sdd_to_psdd(sdd):
    pass