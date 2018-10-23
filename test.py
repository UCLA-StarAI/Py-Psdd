from util import util
from util import data
from algo import algo

def dfs(psdd, asgn, d, l):
    if d == l:        
        res = algo.compute_probability(psdd, asgn)
        print(asgn, res)
        return res
    res = 0.0
    if d < 3:
        res += dfs(psdd, asgn + (True, ), d + 1, l)
        res += dfs(psdd, asgn + (False, ), d + 1, l)
    else:
        res += dfs(psdd, asgn + (None, ), d + 1, l)
    return res

if __name__ == '__main__':
    sdd = util.sdd_from_file('./examples/big-swap.sdd', './examples/big-swap.vtree')
    print(sdd.base)
    psdd = util.sdd_to_psdd(sdd=sdd)
    data_set = data.DataSet(train_data_file="./examples/data.txt")
    psdd.data = data_set.train
    algo.compute_parameter(psdd)
    print(psdd.base)
    util.psdd_to_file(psdd, './examples/big-swap.psdd')
    print("log_ll: ", algo.compute_log_likelihood(psdd, data_set.train))
    print("Check: {}".format(dfs(psdd, (None, ), 0, data_set.dim)))


