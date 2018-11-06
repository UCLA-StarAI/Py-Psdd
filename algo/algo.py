from structure.Psdd import *
from structure.Element import *

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
            res += compute_probability(p, asgn, d + 1) * compute_probability(s, asgn, d + 1) * theta

    return res

def compute_log_likelihood(u, data):
    res = 0.0
    for asgn, w in data.items():
        res += w * math.log(compute_probability(u, asgn))
    return res