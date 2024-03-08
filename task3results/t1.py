import ast
import astunparse

class Inst:
    def instrument_assertion(self, test_file, test_name, assertion_line):
        with open(test_file, 'r') as file:
            tree = ast.parse(file.read())

        test_function = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == test_name:
                test_function = node
                break

        if test_function:
            for statement in test_function.body:
                if isinstance(statement, ast.Assert) and statement.lineno == assertion_line:
                    variables = self.extract_variables(statement.test)
                    for variable in variables:
                        
                        log_statement = ast.Expr(value=
                            ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
                                     args=[ast.Constant("log>>>", kind=None), variable],
                                     keywords=[])) 

                        test_function.body.insert(test_function.body.index(statement), log_statement)
                    break

        with open(test_file[:-3] + "_logged.py", 'w') as output_file:
            output_file.write(astunparse.unparse(tree))

    def extract_variables(self, node):
        variables = set()
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Name):
                variables.add(sub_node)
        return variables

if __name__ == "__main__":
    instrumentor = Inst()
    instrumentor.instrument_assertion("task3results/assertions.py", "test_func", 8)
