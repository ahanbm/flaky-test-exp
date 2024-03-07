import importlib.util
import numpy as np
import types

def execute_test(file_name, test_name, assertion_line):
    spec = importlib.util.spec_from_file_location(test_name, file_name)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)

    # Inject seed-setting logic at the beginning of the test function
    test_code = test_module.__dict__.get(test_name)
    if test_code:
        test_code_ast = test_code.__code__
        test_module.__dict__[test_name] = inject_seed_setting(test_code_ast, test_module)
    
    test_module.test_function()

def inject_seed_setting(test_code_ast, test_module):
    # Construct AST node for setting random seed
    seed_setting_code = ast.parse("np.random.seed(42)")
    
    # Add the seed-setting code to the beginning of the test function
    new_test_body = [seed_setting_code] + list(test_code_ast.co_consts)
    
    # Create a new code object with modified test body
    new_code = types.CodeType(
        test_code_ast.co_argcount,
        test_code_ast.co_kwonlyargcount,
        test_code_ast.co_nlocals,
        test_code_ast.co_stacksize,
        test_code_ast.co_flags,
        b''.join(new_test_body),
        test_code_ast.co_consts,
        test_code_ast.co_names,
        test_code_ast.co_varnames,
        test_code_ast.co_filename,
        test_code_ast.co_name,
        test_code_ast.co_firstlineno,
        test_code_ast.co_lnotab,
        test_code_ast.co_freevars,
        test_code_ast.co_cellvars
    )
    
    # Create a new function object with modified code object
    new_function = types.FunctionType(
        new_code,
        test_module.__dict__,
        test_name
    )
    
    return new_function

if __name__ == "__main__":
    execute_test("test_file.py", "test_function", "assertion_line")
