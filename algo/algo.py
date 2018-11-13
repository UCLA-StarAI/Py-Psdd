from structure.Psdd import *
from structure.Element import *
from structure.Sdd import *

import math
import random

def _satisfy(u, asgn, f):
    if u._idx in f:
        return f[u._idx]

    if u.is_terminal:
        if u._lit == 'F':
            f[u._idx] = False
            return False
        if u._lit == 'T':
            f[u._idx] = True
            return True
        if isinstance(u._lit, int):
            res = asgn[abs(u._lit)]
            if u._lit < 0:
                res = not res
            f[u._idx] = res
            return res

    for e in u._elements:
        if _satisfy(e._prime, asgn, f):
            if _satisfy(e._sub, asgn, f):
                f[u._idx] = True
                return True
            else:
                f[u._idx] = False
                return False

def _add_weight(u, asgn, w, f, g, h):
    if u._idx not in g:
        u._context_weight += w
        g[u._idx] = True
    if u.is_terminal:
        if u._lit == 'T':
            if asgn[list(u._vtree.variables)[0]] and (u._idx not in h):
                u._weight += w
                h[u._idx] = True
    else:
        for e in u._elements:
            p, s = e._prime, e._sub
            if (p._idx in f) and f[p._idx]:
                e._weight += w
                _add_weight(p, asgn, w, f, g, h)
                _add_weight(s, asgn, w, f, g, h)

def set_data(u, data):
    if data is not None:
        set_data(u, None)
        for asgn, w in data.items():
            f, g, h = {}, {}, {}
            _satisfy(u, asgn, f)
            _add_weight(u, asgn, w, f, g, h)

    if data is None:
        u._weight = 0.0
        u._context_weight = 0.0
        for e in u._elements:
            e._theta = 0.0
            e._weight = 0.0
            set_data(e._prime, None)
            set_data(e._sub, None)

def compute_parameter(u):
    ele_cnt = len(u._elements)
    for e in u._elements:
        p, s = e._prime, e._sub
        e._theta = 0.0
        if u._context_weight != 0.0:
            e._theta = e._weight / u._context_weight
        compute_parameter(p)
        compute_parameter(s)

    if u.is_terminal and u._lit == 'T':
        u._theta = 0.0
        if u._context_weight != 0.0:
            u._theta = u._weight / u._context_weight

def compute_probability(u, asgn, d=0):
    flag = False
    for x in u.vtree.variables:
        if asgn[x] is not None:
            flag = True
            break
    if flag == False:
        return 1.0

    res = None
    if u.is_terminal:
        if u._lit == 'F':
            res = 0.0

        if u._lit == 'T':
            v = list(u.vtree.variables)[0]
            res = u._theta if asgn[v] else (1.0 - u._theta)

        if isinstance(u._lit, int):
            v = abs(u._lit)
            sgn = 1 if u._lit > 0 else -1
            asgn_v = 1 if asgn[v] == True else -1
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

def EM(psdd0, psdd1, data):
    data0 = {}
    data1 = {}
    for asgn, w in data.items():
        q = random.gauss(0.5, 0.15)
        q = min(q, 0.99)
        q = max(q, 0.01)
        data0[asgn] = w * (1 - q)
        data1[asgn] = w * q

    set_data(psdd0, data0)
    set_data(psdd1, data1)
    compute_parameter(psdd0)
    compute_parameter(psdd1)

    for i in range(1000):
        # structure learning
        for j in range(50):
            W0, W1 = 0.0, 0.0
            for asgn, w in data0.items():
                W0 += w
            for asgn, w in data1.items():
                W1 += w
            p0 = W0 / (W0 + W1)
            p1 = W1 / (W0 + W1)

            for asgn, w in data.items():
                q0 = compute_probability(psdd0, asgn)
                q1 = compute_probability(psdd1, asgn)
                r0 = q0 * p0
                r1 = q1 * p1
                w0 = r0 / (r0 + r1)
                w1 = r1 / (r0 + r1)
                data0[asgn] = w0 * w
                data1[asgn] = w1 * w

            set_data(psdd0, data0)
            set_data(psdd1, data1)
            compute_parameter(psdd0)
            compute_parameter(psdd1)

def re_index(u, next_idx=0):
    u._idx = next_idx
    next_idx += 1
    for p, s in u._elements:
        next_idx = re_index(p, next_idx)
        next_idx = re_index(s, next_idx)
    return next_idx

def negate(u):
    if u.is_terminal:
        if isinstance(u._lit, int):
            u._lit = -u._lit
        if u._lit == 'T':
            u._lit = 'F'
        if u._lit == 'F':
            u._lit = 'T'
        return None

    for p, s in u._elements:
        negate(s)

def apply(u1, u2, op, cache): # bug with cache
    idx1, idx2 = u1.idx, u2.idx
    if (idx1, idx2, op) in cache:
        return cache[(idx1, idx2, op)]

    if u1.is_terminal and u2.is_terminal:
        b = None
        b1, b2 = u1._lit, u2._lit
        if isinstance(b2, int):
            b1, b2 = b2, b1

        if isinstance(b1, int):
            if isinstance(b2, int):
                if op == 'AND':
                    b = 'F' if b1 == -b2 else b1
                if op == 'OR':
                    b = 'T' if b1 == -b2 else b1
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

        res = Sdd(0, b, u1.vtree)
        cache[(idx1, idx2, op)] = res
        return res

    res = Sdd(0, None, u1.vtree)
    for p, s in u1._elements:
        for q, t in u2._elements:
            r = apply(p, q, 'AND', cache)
            u = apply(s, t, op, cache)
            res.add_element((r, u))

    cache[(idx1, idx2, op)] = res
    return res

def normalize(u, v):
    if v.left is None:
        u.vtree = v
        return u

    ul = u.lit
    if ul == 'T' or ul == 'F':
        u.vtree = v
        u.lit = None
        u.add_element((Sdd(0, 'T', v.left), Sdd(0, ul, v.right)))
    elif u.vtree.idx != v.idx:
        w = u.vtree
        while w.parent.idx != v.idx:
            w = w.parent

        res = Sdd()
        res.vtree = v
        flag = None
        if v.left is w:
            p1, p2 = u, u.copy()
            negate(p2)
            res.add_element((p1, Sdd(0, 'T', v.right)))
            res.add_element((p2, Sdd(0, 'F', v.right)))

        if v.right is w:
            res.add_element((Sdd(0, 'T', v.left), u))
        u = res

    tmp = []
    for p, s in u._elements:
        q = normalize(p, u.vtree.left)
        t = normalize(s, u.vtree.right)
        tmp.append((q, t))
    u._elements = tmp

    return u

def compile(cnf, vtree):
    def f(v):
        if v.is_terminal:
            return { v._var: v }
        return { **f(v.left), **f(v.right) }
    m = f(vtree)

    def test(x):
        if (len(x._elements) == 0) and (x._lit == None):
            return 'ERROR'
        for p, s in x._elements:
            res = test(p)
            if res is not None:
                return res
            res = test(s)
            if res is not None:
                return res
        return None

    cache = {}
    ri = Sdd(0, 'T')
    ri = normalize(ri, vtree)
    ri._node_count = re_index(ri)
    for clause in cnf:
        rj = Sdd(0, 'F')
        rj = normalize(rj, vtree)
        rj._node_count = re_index(rj)
        for lit in clause:
            rk = Sdd(0, lit, m[abs(lit)])
            rk = normalize(rk, vtree)
            rk._node_count = re_index(rk)

            cache.clear()
            rj = apply(rj, rk, 'OR', cache)
            rj._node_count = re_index(rj)

        cache.clear()
        ri = apply(ri, rj, 'AND', cache)
        ri._node_count = re_index(ri)

    return ri