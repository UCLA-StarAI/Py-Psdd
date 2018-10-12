from util import util
from util import data

if __name__ == '__main__':    
    sdd = util.sdd_from_file('./examples/big-swap.sdd', './examples/big-swap.vtree')    
    print(sdd.base)
    psdd = util.sdd_to_psdd(sdd=sdd)    
    data_set = data.DataSet(train_data_file="./examples/data.txt")
    psdd.data = data_set.train
    psdd.calculate_parameter()    
    print(psdd.base)
    