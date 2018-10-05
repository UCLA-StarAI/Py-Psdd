from util import util

if __name__ == '__main__':    
    sdd = util.sdd_from_file('./examples/big-swap.sdd', './examples/big-swap.vtree')    
    psdd = util.sdd_to_psdd(sdd=sdd)
    print(psdd.base)
    