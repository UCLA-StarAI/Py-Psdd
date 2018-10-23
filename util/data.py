class DataSet(object):

    def __init__(self, train_data_file=None,
                    valid_data_file=None, test_data_file=None):
        self._dim = None
        self._train = None
        self._valid = None
        self._test = None
        if train_data_file is not None:
            self._train = self.read_data(train_data_file)
        if valid_data_file is not None:
            self._valid = self.read_data(valid_data_file)
        if test_data_file is not None:
            self._test = self.read_data(test_data_file)    

    @property
    def dim(self):
        return self._dim

    @property
    def train(self):
        return self._train

    @property
    def valid(self):
        return self._valid

    @property
    def test(self):
        return self._test

    def read_data(self, file_name):
        data = {}
        with open(file_name, 'r') as f:
            for line in f:
                if line[-1] == '\n':
                    line = line[:-1]

                head, tail = line.split('|', 1)

                w = float(head)
                d = [ (x == '1') for x in tail.split(',') ]
                asgn = (None, )
                for x in d:
                    asgn = asgn + (x, )

            if asgn not in data:
                data[asgn] = 0            

            data[asgn] = data[asgn] + w

            self._dim = len(asgn) - 1

        return data