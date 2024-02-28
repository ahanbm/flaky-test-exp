import importlib.util

def execute_test(file_name, test_name, assertion_line):
    spec = importlib.util.spec_from_file_location(test_name, file_name)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)

    test_module.test_function()

if __name__ == "__main__":
    execute_test("test_file.py", "test_function", "assertion_line")
