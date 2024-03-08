
import numpy as np

def test_func():
    x = 0.5
    y = 0.6
    assert (x < y)

def test_func2():
    random_numbers = np.random.rand(5)
    assert (np.sum(random_numbers) > 1.0)
if (__name__ == '__main__'):
    test_func()
    test_func2()
