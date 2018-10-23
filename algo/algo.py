from structure.Psdd import *
from structure.Element import *

import math

def compute_parameter(u):
    ele_cnt = len(u._elements)
    for i, e in enumerate(u._elements):
        p, s, theta = e._prime, e._sub, e._theta
        theta = (p._weight + 1.0) / (p._context_weight + 1.0 * float(ele_cnt))
        u._elements[i] = Element(p, s, theta)

        compute_parameter(p)
        compute_parameter(s)

    if u._base == 'True':
        u._theta = (u._weight + 1.0) / (u._context_weight + 1.0)

def compute_probability(u, asgn):
    flag = False
    for x in u.vtree.variables:
        if asgn[x] is not None:
            flag = True
            break
    if flag is False:
        return 1.0

    res = None
    if u.is_leaf:
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
            res += compute_probability(p, asgn) * compute_probability(s, asgn) * theta

    return res

def compute_log_likelihood(u, data):
    res = 0.0
    for asgn, w in data.items():
        res += w * math.log(compute_probability(u, asgn))
    return res