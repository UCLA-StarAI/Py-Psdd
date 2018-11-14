from algo import algo
from util import util
from util import data

import random
import sys
import os

task_name = ''
train_data_file = ''
valid_data_file = ''
sample_file = ''
vtree_file = ''
cnf_file = ''
sdd_file = ''
psdd0_file = ''
psdd1_file = ''

def init():
    if len(sys.argv) < 2:
        print('usage: python ensemble.py [name of the task]')
        sys.exit(1)

    global task_name
    global train_data_file
    global valid_data_file
    global sample_file
    global vtree_file
    global cnf_file
    global sdd_file
    global psdd0_file
    global psdd1_file

    task_name = sys.argv[1]
    train_data_file = './workspace/{}.train'.format(task_name)
    valid_data_file = './workspace/{}.valid'.format(task_name)
    sample_file = './workspace/{}.sample'.format(task_name)
    vtree_file = './workspace/{}.vtree'.format(task_name)
    cnf_file = './workspace/{}.cnf'.format(task_name)
    sdd_file = './workspace/{}.sdd'.format(task_name)
    psdd0_file = './workspace/{}.psdd.0'.format(task_name)
    psdd1_file = './workspace/{}.psdd.1'.format(task_name)

def preprocess():
    # generate data set
    n, m = None, None
    with open('./workspace/{}.label_matrix'.format(task_name), 'r') as f, \
         open(train_data_file, 'w') as t, \
         open(valid_data_file, 'w') as v, \
         open(sample_file, 'w') as o:
        n, m = [ int(x) for x in f.readline().strip().split() ]
        for line in f:
            example = [ int(x) for x in line.strip().split(' ', m) ]
            s = ''
            for x in example:
                if x == 0:
                    s += '0,0,'
                if x == 1:
                    s += '0,1,'
                if x == -1:
                    s += '1,1,'
            s = s[:-1] + '\n'
            if random.uniform(0, 1) > 0.2:
                t.write(s)
            else:
                v.write(s)
            o.write(s)
            
    exit(0)
    # learn_vtree
    # os.system('java -jar ./lib/psdd.jar learnVtree -d ./workspace/{} -o ./workspace/ -e'.format(train_data_file))
    # os.system('mv ./workspace/.vtree ./workspace/{}'.format(vtree_file))

    # gen_cnf
    with open('./workspace/{}.cnf'.format(task_name), 'w') as c:
        c.write('p cnf {} {}\n'.format(m * 2, m))
        for i in range(1, m + 1):
            c.write('{} {} 0\n'.format(-(2 * i - 1), 2 * i))

    # compile_sdd
    # os.system('./lib/sdd-linux -c {} -v {} -R {} -r 0'.format(cnf_file, vtree_file, sdd_file))

    # generate initial psdds
    vtree = util.vtree_from_file(vtree_file)
    print(vtree.left.idx, vtree.right.idx)
    sdd = util.sdd_from_file(sdd_file, vtree_file)
    print(len(sdd._elements))
    sdd = algo.normalize(sdd, vtree)
    print(len(sdd._elements))
    exit(0)
    sdd._node_count = algo.re_index(sdd)
    util.psdd_to_file(psdd0, psdd0_file)
    psdd1 = util.sdd_to_psdd(sdd)
    data_set = data.DataSet(train_data_file=train_data_file, valid_data_file=valid_data_file)

    return psdd0, psdd1, data_set

def compute_ensemble_log_likelihood(psdd0, p0, psdd1, p1, data):
    ll = 0.0
    for asgn, w in data.items():
        q0 = algo.compute_probability(psdd0, asgn) * p0
        q1 = algo.compute_probability(psdd1, asgn) * p1
        ll += w * math.log(q0 + q1)
    return ll

def EM(psdd0, psdd1, data_set):
    train = data_set.train
    valid = data_set.valid
    data0 = {}
    data1 = {}
    for asgn, w in train.items():
        q = random.gauss(0.5, 0.15)
        q = min(q, 0.99)
        q = max(q, 0.01)
        data0[asgn] = w * (1 - q)
        data1[asgn] = w * q

    algo.set_data(psdd0, data0)
    algo.set_data(psdd1, data1)
    algo.compute_parameter(psdd0)
    algo.compute_parameter(psdd1)

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

            for asgn, w in train.items():
                q0 = algo.compute_probability(psdd0, asgn)
                q1 = algo.compute_probability(psdd1, asgn)
                r0 = q0 * p0
                r1 = q1 * p1
                w0 = r0 / (r0 + r1)
                w1 = r1 / (r0 + r1)
                data0[asgn] = w0 * w
                data1[asgn] = w1 * w

            algo.set_data(psdd0, data0)
            algo.set_data(psdd1, data1)
            algo.compute_parameter(psdd0)
            algo.compute_parameter(psdd1)

            train_ll = compute_ensemble_log_likelihood(psdd0, p0, psdd1, p1, data_set.train)
            valid_ll = compute_ensemble_log_likelihood(psdd0, p0, psdd1, p1, data_set.valid)

            print('{} {}, train_ll: {} valid_ll: {}', train_ll, valid_ll)

if __name__ == '__main__':
    init()
    psdd0, psdd1, data_set = preprocess()
    EM(psdd0, psdd1, data_set)