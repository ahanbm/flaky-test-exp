import ast
import astunparse

class Instrumentor:
    def instrument_assertion(self, test_file, test_name, assertion_line):
        with open(test_file, 'r') as file:
            tree = ast.parse(file.read())

        # Find the specified test function/method
        test_function = None
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == test_name:
                test_function = node
                break

        if test_function:
            # Find the specified assertion line within the test function
            for statement in test_function.body:
                if isinstance(statement, ast.Assert) and statement.lineno == assertion_line:
                    # Extract variables involved in the assertion
                    variables = self.extract_variables(statement.test)
                    # Insert logging statements before the assertion
                    for variable in variables:
                        
                        log_statement = ast.Expr(value=
                            ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
                                     args=[ast.Constant("log>>>", kind=None), variable],
                                     keywords=[], 
                                     _str="hello")) 
                        
                        '''
                        log_statement = ast.Expr(value=ast.Call(
                            func=ast.Name(id='print', ctx=ast.Load()),  
                            args=[ast.Constant(value='Hello, world!', kind=None)], 
                            keywords=[],
                        ))
                        '''

                        test_function.body.insert(test_function.body.index(statement), log_statement)
                    break

        # Write the modified code to a new file
        with open(test_file[:-3] + "_instrumented.py", 'w') as output_file:
            output_file.write(astunparse.unparse(tree))

    def extract_variables(self, node):
        variables = set()
        # Traverse the AST to extract variables
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Name):
                variables.add(sub_node)
            # TODO: Add additional cases for handling more complex objects
        return variables

# Usage example
if __name__ == "__main__":
    instrumentor = Instrumentor()
    instrumentor.instrument_assertion("task3results/assertions.py", "func", 6)
    instrumentor.instrument_assertion("task3results/assertions.py", "func2", 10)