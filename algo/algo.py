from structure.Psdd import *
from structure.Element import *

def calculate_parameter(u):
    ele_cnt = len(u._elements)
    for i, e in enumerate(u._elements):
        p, s, theta = e._prime, e._sub, e._theta
        theta = (p._weight + 1.0) / (p._context_weight + float(ele_cnt))
        u._elements[i] = Element(p, s, theta)        

        calculate_parameter(p)
        calculate_parameter(s)

    if u.is_leaf:
        u._theta = (u._weight + 1.0) / (u._context_weight + 1.0)

def calculate_probability(u, asgn):
    
    pass