from util import util
from util import data
from algo import algo
from structure.Sdd import *

def dfs(psdd, asgn, d, l):
    if d == l:
        res = algo.compute_probability(psdd, asgn)
        return res
    res = 0.0
    # if d < 3:
    res += dfs(psdd, asgn + (True, ), d + 1, l)
    res += dfs(psdd, asgn + (False, ), d + 1, l)
    # else:
        # res += dfs(psdd, asgn + (None, ), d + 1, l)
    return res

if __name__ == '__main__':
    sdd = algo.compile(util.cnf_from_file('./examples/big-swap.cnf'), util.vtree_from_file('./examples/big-swap.vtree'))
    psdd = util.sdd_to_psdd(sdd)
    data_set = data.DataSet(train_data_file="./examples/big-swap.data")
    algo.set_data(psdd, data_set.train)
    algo.compute_parameter(psdd)
    util.psdd_to_file(psdd, './examples/big-swap.psdd')
    # sdd = util.sdd_from_file('./examples/big-swap.sdd', './examples/big-swap.vtree')
    # sdd = algo.normalize(sdd, util.vtree_from_file('./examples/big-swap.vtree'))
    # sdd.node_count = algo.re_index(sdd)
    # psdd = util.sdd_to_psdd(sdd)
    # data_set = data.DataSet(train_data_file="./examples/big-swap.data")
    # algo.set_data(psdd, data_set.train)
    # algo.compute_parameter(psdd)
    # util.psdd_to_file(psdd, './examples/big-swap.psdd')
    # print("log_ll: ", algo.compute_log_likelihood(psdd, data_set.train))
    print("Check: {}".format(dfs(psdd, (None, ), 0, data_set.dim)))