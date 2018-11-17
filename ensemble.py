from algo import algo
from util import util
from util import data

import random
import sys
import os
import math

task_name = ''
train_data_file = ''
valid_data_file = ''
sample_file = ''
vtree_file = ''
cnf_file = ''
sdd_file = ''
psdd0_file = ''
psdd1_file = ''
label0_file = ''
label1_file = ''

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
    global label0_file
    global label1_file

    task_name = sys.argv[1]
    train_data_file = './workspace/{}.train'.format(task_name)
    valid_data_file = './workspace/{}.valid'.format(task_name)
    sample_file = './workspace/{}.sample'.format(task_name)
    vtree_file = './workspace/{}.vtree'.format(task_name)
    cnf_file = './workspace/{}.cnf'.format(task_name)
    sdd_file = './workspace/{}.sdd'.format(task_name)
    psdd0_file = './workspace/{}.psdd.0'.format(task_name)
    psdd1_file = './workspace/{}.psdd.1'.format(task_name)
    label0_file = './workspace/{}.label.0'.format(task_name)
    label1_file = './workspace/{}.label.1'.format(task_name)

def preprocess():
    # generate data set
    print('generating data set...')
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

    # learn_vtree
    print('learning vtree from data...')
    os.system('java -jar ./lib/psdd.jar learnVtree -d {} -o ./workspace/'.format(train_data_file))
    os.system('mv ./workspace/.vtree {}'.format(vtree_file))

    # gen_cnf
    print('generating cnf...')
    with open('./workspace/{}.cnf'.format(task_name), 'w') as c:
        c.write('p cnf {} {}\n'.format(m * 2, m))
        for i in range(1, m + 1):
            c.write('{} {} 0\n'.format(-(2 * i - 1), 2 * i))

    # compile_sdd
    print('compiling sdd...')
    os.system('./lib/sdd-linux -c {} -v {} -R {} -r 0'.format(cnf_file, vtree_file, sdd_file))

    # generate initial psdds
    print('generating psdds...')
    vtree = util.vtree_from_file(vtree_file)
    sdd = util.sdd_from_file(sdd_file, vtree_file)
    cache_lit, cache_idx = {}, {}
    sdd = algo.normalize(sdd, vtree, cache_lit, cache_idx)
    sdd._node_count = algo.re_index(sdd)
    cache = {}
    psdd0 = util.sdd_to_psdd(sdd, cache)
    cache = {}
    psdd1 = util.sdd_to_psdd(sdd, cache)
    data_set = data.DataSet(train_data_file=train_data_file, valid_data_file=valid_data_file)

    return psdd0, psdd1, data_set

def compute_ensemble_log_likelihood(psdd0, p0, psdd1, p1, data):
    ll = 0.0
    asgn_batch = [ asgn for asgn, w in data.items() ]
    w_batch = [ w for asgn, w in data.items() ]    

    cache = {}
    Q0 = algo.compute_probability_batch(psdd0, asgn_batch, cache)
    cache = {}
    Q1 = algo.compute_probability_batch(psdd1, asgn_batch, cache)

    ll = sum(w * math.log(q0 * p0 + q1 * p1) for q0, q1, w in zip(Q0, Q1, w_batch))
    # for asgn, w in data.items():
    #     q0 = algo.compute_probability(psdd0, asgn) * p0
    #     q1 = algo.compute_probability(psdd1, asgn) * p1
    #     ll += w * math.log(q0 + q1)
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

    count = 0
    for i in range(1):
        # structure learning
        for j in range(100):
            W0, W1 = 0.0, 0.0
            for asgn, w in data0.items():
                W0 += w
            for asgn, w in data1.items():
                W1 += w
            p0 = W0 / (W0 + W1)
            p1 = W1 / (W0 + W1)

            asgn_batch = [ asgn for asgn, w in train.items() ]
            w_batch = [ w for asgn, w in train.items() ]

            cache = {}
            Q0 = algo.compute_probability_batch(psdd0, asgn_batch, cache)
            cache = {}
            Q1 = algo.compute_probability_batch(psdd1, asgn_batch, cache)

            Q0 = [ x * p0 / (x * p0 + y * p1) for x, y in zip(Q0, Q1) ]
            for q0, asgn, w in zip(Q0, asgn_batch, w_batch):
                data0[asgn] = q0 * w
                data1[asgn] = (1.0 - q0) * w
            # for asgn, w in train.items():
            #     q0 = algo.compute_probability(psdd0, asgn)
            #     q1 = algo.compute_probability(psdd1, asgn)
            #     r0 = q0 * p0
            #     r1 = q1 * p1
            #     w0 = r0 / (r0 + r1)
            #     w1 = r1 / (r0 + r1)
            #     data0[asgn] = w0 * w
            #     data1[asgn] = w1 * w

            algo.set_data(psdd0, data0)
            algo.set_data(psdd1, data1)
            algo.compute_parameter(psdd0)
            algo.compute_parameter(psdd1)

            train_ll = compute_ensemble_log_likelihood(psdd0, p0, psdd1, p1, data_set.train)
            valid_ll = compute_ensemble_log_likelihood(psdd0, p0, psdd1, p1, data_set.valid)

            print('{} {}, train_ll: {} valid_ll: {}'.format(i, j, train_ll, valid_ll))
            with open('./workspace/log.txt', 'a') as f:
                f.write('{} {} {}\n'.format(count, train_ll, valid_ll))
            count += 1

    W0, W1 = 0.0, 0.0
    for asgn, w in data0.items():
        W0 += w
    for asgn, w in data1.items():
        W1 += w
    p0 = W0 / (W0 + W1)
    p1 = W1 / (W0 + W1)

    util.psdd_to_file(psdd0, psdd0_file)
    util.psdd_to_file(psdd1, psdd1_file)

    return psdd0, psdd1, p0, p1

def generate_labels(psdd0, psdd1, p0, p1):
    label0 = []
    label1 = []
    with open(sample_file, 'r') as f:
        for line in f:
            line = line.strip()
            d = [ (x == '1') for x in line.split(',') ]
            asgn = (None, )
            for x in d:
                asgn = asgn + (x, )
            q0 = algo.compute_probability(psdd0, asgn)
            q1 = algo.compute_probability(psdd1, asgn)
            l0 = (q1 * p1) / (q0 * p0 + q1 * p1)
            l1 = (q0 * p0) / (q0 * p0 + q1 * p1)
            label0.append(l0)
            label1.append(l1)

    with open(label0_file, 'w') as f:
        for x in label0:
            f.write('{}\n'.format(x))

    with open(label1_file, 'w') as f:
        for x in label1:
            f.write('{}\n'.format(x))

if __name__ == '__main__':
    init()
    psdd0, psdd1, data_set = preprocess()
    psdd0, psdd1, p0, p1 = EM(psdd0, psdd1, data_set)
    generate_labels(psdd0, psdd1, p0, p1)