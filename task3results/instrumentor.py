import argparse
import t1
import t2

class Instrumentor:
    def __init__(self):
        self.a = t1.Inst()
        self.b = t2.Inst()

    def instrument_assertion(self, test_file, test_name, assertion_line=None):
        self.a.instrument_assertion(test_file, test_name, assertion_line)
        self.b.instrument_assertion((test_file[:-3] + "_logged.py"), test_name)
        
        self.b.execute_test(test_file, test_name)
        self.b.execute_test((test_file[:-3] + "_final.py"), test_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Instrument assertions in a test file.")
    parser.add_argument("--test_file", type=str, default = "library_assertions.py", help="Path to the test file.")
    parser.add_argument("--test_name", type=str, default = "test_instrumentation", help="Name of the test function.")
    parser.add_argument("--assertion_line", type=int, default=None, help="Line number of the assertion to instrument.")
    
    args = parser.parse_args()
    
    instrumentor = Instrumentor()
    instrumentor.instrument_assertion(args.test_file, args.test_name, args.assertion_line)
