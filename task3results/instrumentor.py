import t1
import t2

class Instrumentor:
    a = t1.Inst()
    b = t2.Inst()

    def instrument_assertion(self, test_file, test_name, assertion_line):
        self.a.instrument_assertion(test_file, test_name, assertion_line)
        self.b.instrument_assertion((test_file[:-3] + "_logged.py"), test_name)
        self.b.execute_test((test_file[:-3] + "_logged.py"), test_name)

if __name__ == "__main__":
    instrumentor = Instrumentor()
    instrumentor.instrument_assertion("task3results/assertions.py", "test_func", 9)