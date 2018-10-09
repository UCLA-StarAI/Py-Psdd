from structure.Element import Element
import copy

class Split(Primitive):

    def __init__(self, element_to_split, variable_to_split, depth):
        self._element_to_split = element_to_split
        self._variable_to_split = variable_to_split
        self._depth = depth

    @property
    def element_to_split(self):
        return self._element_to_split

    @property
    def variable_to_split(self):
        return self._variable_to_split

    @property
    def depth(self):
        return self._depth

    def execute(self):
        parent = self.element_to_split.parent
        original_element, copied_element = self._copy_and_modify_element_for_split(self._element_to_split, 0)
        if original_element is None or copied_element is None:
            raise ValueError("Split elements become invalid.")
        parent.add_element(copied_element)

    def _copy_and_modify_element_for_split(self, original_element, current_depth):
        original_element.remove_splittable_variable(self.variable_to_split)
        original_prime = original_element.prime
        original_sub = original_element.sub
        if current_depth >= self._depth:
            if self._variable_to_split in original_prime.vtree.variables:
                original_prime, copied_prime = self._copy_and_modify_node_for_split(original_prime, current_depth)
                copied_sub = original_sub
            elif self._variable_to_split in original_sub.vtree.variables:
                original_sub, copied_sub = self._copy_and_modify_node_for_split(original_sub, current_depth)
                copied_prime = original_prime
            else:
                copied_prime = original_prime
                copied_sub = original_sub
        else:
            original_prime, copied_prime = self._copy_and_modify_node_for_split(original_prime, current_depth)
            original_sub, copied_sub = self._copy_and_modify_node_for_split(original_sub, current_depth)
        if copied_prime is not None and copied_sub is not None:
            copied_element = Element(copied_prime, copied_sub)
            copied_element.parameter = original_element.parameter
            copied_element.splittable_variables = copy.deepcopy(original_element.splittable_variables)
        else:
            copied_element = None
        if original_prime is not None and original_sub is not None:
            original_element.prime = original_prime
            original_element.sub = original_sub
        else:
            original_element = None
        return original_element, copied_element

    def _copy_and_modify_node_for_split(self, original_node, current_depth):
        raise NotImplementedError()

    def simulate(self):
        raise NotImplementedError()
