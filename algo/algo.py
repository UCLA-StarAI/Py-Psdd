from structure.Psdd import *
from structure.Element import *
from structure.Sdd import *

import math

def compute_parameter(u):
    print(u._idx, u._context_weight, u.weight)
    ele_cnt = len(u._elements)
    for e in u._elements:
        p, s, theta = e._prime, e._sub, None
        if u._context_weight != 0.0:
            theta = (p._context_weight + 0.0) / (u._context_weight + 0.0 * float(ele_cnt))
        else:
            theta = 1e-10

        if theta == 0.0:
            theta = 1e-10
        e.theta = theta

        compute_parameter(p)
        compute_parameter(s)

    if u._base == 'T':
        if u._context_weight != 0.0:
            u._theta = (u._weight + 0.0) / (u._context_weight + 0.0)
            if u._theta == 0.0:
                u._theta = 1e-10
        else:
            u._theta = 1e-10

def compute_probability(u, asgn, d=0):
    flag = False
    for x in u.vtree.variables:
        if asgn[x] is not None:
            flag = True
            break
    if flag is False:
        return 1.0

    res = None
    if u.is_terminal:
        if u._base == 'F':
            res = 0.0

        if u._base == 'T':
            v = list(u.vtree.variables)[0]
            res = u._theta if asgn[v] else (1.0 - u._theta)

        if isinstance(u._base, int):
            v = abs(u._base)
            sgn = 1 if u._base > 0 else -1
            asgn_v = 1 if asgn[v] is True else -1
            res = 1.0 if sgn * asgn_v > 0 else 0.0
    else:
        res = 0.0
        for e in u._elements:
            p, s, theta = e._prime, e._sub, e._theta
            res += compute_probability(p, asgn, d + 1) * compute_probability(s, asgn, d + 1) * theta

    return res

def compute_log_likelihood(u, data):
    res = 0.0
    for asgn, w in data.items():
        res += w * math.log(compute_probability(u, asgn))
    return res

def negate(u):
    if u.is_terminal:
        if isinstance(u._base, int):
            u._base = -u._base
        if u._base == 'T':
            u._base = 'F'
        if u._base == 'F':
            u._base = 'T'
        return None

    for p, s in u._elements:
        negate(s)

def apply(u1, u2, op, next_idx=0, cache={}):
    idx1, idx2 = u1.idx, u2.idx
    if (idx1, idx2, op) in cache:
        return cache[(idx1, idx2, op)], next_idx
    if (idx2, idx1, op) in cache:
        return cache[(idx2, idx1, op)], next_idx

    res = None
    if u1.is_terminal and u2.is_terminal:
        b = None
        b1, b2 = u1._base, u2._base
        if isinstance(b2, int):
            b1, b2 = b2, b1

        if isinstance(b1, int):
            if isinstance(b2, int):
                if op == 'AND':
                    b = 'F' if b1 * b2 < 0 else b1
                if op == 'OR':
                    b = 'T' if b1 * b2 < 0 else b1
            else:
                if op == 'AND':
                    b = b1 if b2 == 'T' else 'F'
                if op == 'OR':
                    b = 'T' if b2 == 'T' else b1
        else:
            if op == 'AND':
                b = 'F' if b1 == 'F' else b2
            if op == 'OR':
                b = 'T' if b1 == 'T' else b2            

        res = Sdd(idx=next_idx, base=b, vtree=u1.vtree)
        next_idx += 1
        return res, next_idx

    res = Sdd(idx=next_idx, base=None, vtree=u1.vtree)
    for p, s in u1._elements:
        for q, t in u2._elements:
            r, next_idx = apply(p, q, 'AND', next_idx, cache)
            u, next_idx = apply(s, t, op, next_idx, cache)
            res.add_element((r, u))
    return res    

def normalize(u, v, next_idx):

    if u.is_terminal:
        if isinstance(u._base, int):
            var = u._base
            u._base = None

            if abs(var) in v.left.variables:
                u.add_element

        return None

def compile(cnf, vtree):
    ri = Sdd(0, 'T', vtree)
    for clause in cnf:
        rj = Sdd(0, 'T', vtree)
        for lit in clause:
            rk = Sdd(0, lit, vtree)
            rk = normalize(rk, vtree, 1)
            rj = apply(rj, rk, 'OR')
        ri = apply(ri, rj, 'AND')
    return ri