class Sdd(object):

    def __init__(self, vtree):
        self._id = -1
        self._vtree = None
        self._var = None
        self._elements = []        

    def add_element(self, element):
        self._elements.append(element)

    
