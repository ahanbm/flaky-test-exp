
import numpy as np

class Tests():

    def func(self):
        x = 0.5
        y = 0.6
        assert (x < y)

    def func2(self):
        random_numbers = np.random.rand(5)
        assert (np.sum(random_numbers) > 1.0)
if (__name__ == '__main__'):
    Tester = Tests()
    Tester.func()
    Tester.func2()
