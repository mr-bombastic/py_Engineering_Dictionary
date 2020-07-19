from logic import *  # will import all classes in that document
from constant import *  # will import all classes in that document
from variable import *  # will import all classes in that document
from equation import *  # will import all classes in that document
from theory import *  # will import all classes in that document


class Method(Logic):
    def __init__(self, name, description, steps):  # constructor for class
        self._name = name
        self._description = description
        self._steps = steps

    def get_step(self, i):
        if i < len(self._steps):
            return self._steps[i]
        else:
            return False

    def get_num_steps(self):
        return len(self._steps)

    def get_steps(self):
        return self._steps
