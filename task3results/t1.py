import ast
import astunparse

class Instrumentor:
    def __init__(self):
        pass

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
                if isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Compare) and statement.lineno == assertion_line:
                    # Extract the variables involved in the assertion
                    variables = self.extract_variables(statement.value)
                    # Insert logging statements before the assertion
                    for variable in variables:
                        log_statement = ast.Expr(ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
                                                           args=[ast.Str(s='log>>>'), variable],
                                                           keywords=[]))
                        test_function.body.insert(test_function.body.index(statement), log_statement)
                    break

        # Output the modified code
        print(astunparse.unparse(tree))

    def extract_variables(self, compare_node):
        variables = set()
        # Traverse the comparison tree to extract variables
        for node in ast.walk(compare_node):
            if isinstance(node, ast.Name):
                variables.add(node.id)
            # You can add additional logic to handle more complex objects like arrays or tensors
        return variables

# Usage example
if __name__ == "__main__":
    instrumentor = Instrumentor()
    instrumentor.instrument_assertion("test_file.py", "test_function", 10)  # Example file, function, and line number
