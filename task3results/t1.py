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
                if statement.lineno == assertion_line and self.is_approx_assertion(statement):

                    left,right = self.extract_comparison_values(statement.test)
                        
                    left_statement = ast.Expr(value=
                        ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
                                    args=[ast.Constant("log>>>", kind=None), left],
                                    keywords=[])) 
                    
                    right_statement = ast.Expr(value=
                        ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
                                    args=[ast.Constant("log>>>", kind=None), right],
                                    keywords=[])) 

                    test_function.body.insert(test_function.body.index(statement), left_statement)
                    test_function.body.insert(test_function.body.index(statement), right_statement)
                    break

        with open(test_file[:-3] + "_logged.py", 'w') as output_file:
            output_file.write(astunparse.unparse(tree))

    def extract_variables(self, node):
        variables = set()
        for sub_node in ast.walk(node):
            if isinstance(sub_node, ast.Name):
                variables.add(sub_node)
        return variables

    def extract_comparison_values(self, assert_node):
        left_value = assert_node.left
        right_value = assert_node.comparators[0]
        return left_value, right_value
    
    def is_approx_assertion(self, assert_node):
        if isinstance(assert_node, ast.Assert):
            if isinstance(assert_node.test, ast.Compare):
                for op in assert_node.test.ops:
                    if not isinstance(op, ast.Eq): 
                        return "assert expr < | > | <= | >= threshold"
        
        if isinstance(assert_node, ast.Expr):
            if isinstance(assert_node.value, ast.Call):
                call_node = assert_node.value
                if isinstance(call_node.func, ast.Attribute):
                    attr_node = call_node.func
                    if isinstance(attr_node.value, ast.Name) and attr_node.value.id == 'self':
                        if isinstance(attr_node.attr, str) and attr_node.attr.startswith('assert'):
                            return attr_node.attr
                        
        elif isinstance(assert_node, ast.FunctionDef):
            for stmt in assert_node.body:
                result = self.is_approx_assertion(stmt)
                if result:
                    return result
                
        elif isinstance(assert_node, ast.ClassDef):
            for base in assert_node.bases:
                result = self.is_approx_assertion(base)
                if result:
                    return result
            
        return None


if __name__ == "__main__":
    instrumentor = Inst()
    instrumentor.instrument_assertion("task3results/assertions.py", "test_func", 11)
