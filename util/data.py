class DataSet(object):

    def __init__(self, dataset_name):
        self._train = None
        self._valid = None
        self._test = None
        pass

    @property
    def train(self):
        return self._train

    @property
    def valid(self):
        return self._valid

    @property
    def test(self):
        return self._test
