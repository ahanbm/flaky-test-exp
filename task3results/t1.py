import ast
import astunparse

class Inst:
    def instrument_assertion(self, test_file, test_name, assertion_line = None):
        with open(test_file, 'r') as file:
            tree = ast.parse(file.read())

        test_function = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == test_name:
                test_function = node
                break

        if test_function:
            modifications = []
            
            for statement in test_function.body:
                if not assertion_line or statement.lineno == assertion_line:
                    left, right = self.assess_approx_assertion(statement)

                    if not left or not right:
                        continue

                    left_statement = ast.Expr(value=ast.Call(
                        func=ast.Name(id='print', ctx=ast.Load()),
                        args=[ast.Constant("log>>>", kind=None), left],
                        keywords=[]
                    ))
                    
                    right_statement = ast.Expr(value=ast.Call(
                        func=ast.Name(id='print', ctx=ast.Load()),
                        args=[ast.Constant("log>>>", kind=None), right],
                        keywords=[]
                    ))

                    modifications.append((test_function.body.index(statement), left_statement, right_statement))

            for index, left_statement, right_statement in reversed(modifications):
                test_function.body.insert(index, left_statement)
                test_function.body.insert(index + 1, right_statement)

        with open(test_file[:-3] + "_logged.py", 'w') as output_file:
            output_file.write(astunparse.unparse(tree))

    def assess_approx_assertion(self, assert_node):
        if isinstance(assert_node, ast.Assert):
            if isinstance(assert_node.test, ast.Compare):
                for op in assert_node.test.ops:
                    if not isinstance(op, ast.Eq):
                        print (ast.dump(assert_node, indent=4))
                        return assert_node.test.left, assert_node.test.comparators[0]
        
        if isinstance(assert_node, ast.Expr):
            if isinstance(assert_node.value, ast.Call):
                call_node = assert_node.value
                if isinstance(call_node.func, ast.Attribute):
                    attr_node = call_node.func
                    if isinstance(attr_node.attr, str) and attr_node.attr.startswith('assert'):
                        return assert_node.value.args[0], assert_node.value.args[1]
        
        elif isinstance(assert_node, ast.FunctionDef):
            for stmt in assert_node.body:
                return self.assess_approx_assertion(stmt)
        
        elif isinstance(assert_node, ast.ClassDef):
            for base in assert_node.bases:
                return self.assess_approx_assertion(base)
        
        return None, None
