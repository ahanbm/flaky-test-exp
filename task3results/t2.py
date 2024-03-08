import importlib.util
import ast
import astunparse

class Inst:
    def numpy_used(self, stmt):
        if isinstance(stmt, ast.Assign):
            # Check if the value being assigned is a function call
            if isinstance(stmt.value, ast.Call):
                # Check if the function being called is from np.random
                if isinstance(stmt.value.func, ast.Attribute):
                    if isinstance(stmt.value.func.value, ast.Attribute):
                        if stmt.value.func.value.attr == "random":
                            return True
        return False
    
    def find_parent_block(self, tree, node):
        """
        Find the parent block of a given node in the AST tree.
        """
        for item in ast.walk(tree):
            if isinstance(item, ast.FunctionDef) and node in item.body:
                return item  # Return the function definition as the parent block
            elif isinstance(item, ast.ClassDef) and node in item.body:
                return item  # Return the class definition as the parent block
            elif isinstance(item, ast.Module) and node in item.body:
                return item
        
        parent_block = None
        for item in ast.walk(tree):
            if isinstance(item, (ast.FunctionDef, ast.ClassDef)) and node in item.body:
                parent_block = item  # Update the parent block if the node is found inside a function or class
            elif isinstance(item, ast.Import) or isinstance(item, ast.ImportFrom):
                # Stop traversing further if an import statement is encountered
                break
        return parent_block

    def instrument_assertion(self, test_file, test_name):
        with open(test_file, 'r') as file:
            tree = ast.parse(file.read())

        # Find the specified test function/method
        test_function = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == test_name:
                test_function = node
                break
        
        #Numpy random.seed
        #TensorFlow random.set_seed
        #TensorFlow set_random_seed
        #TensorFlow random.set_random_seed
        #TensorFlow compat.v1.random.set_random_seed
        #PyTorch manual_seed
        #PyTorch cuda.manual_seed_all
        #PyTorch seed
        #Random (Python) seed

        randoms = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        if test_function:
            # Find the specified assertion line within the test function
            for statement in test_function.body:
                if (self.numpy_used(statement)):
                    randoms[0] = 1

            if randoms[0] == 1:
                seed_statement = ast.Expr(
                    value=ast.Call(
                        func=ast.Attribute(
                            value=ast.Attribute(
                                value=ast.Name(id='np', ctx=ast.Load()),
                                attr='random',
                                ctx=ast.Load()
                            ),
                            attr='seed',
                            ctx=ast.Load()
                        ),
                        args=[ast.Constant(value=42, kind=None)],
                        keywords=[]
                    )
                )
                
                (self.find_parent_block(tree, test_function)).body.insert(0, seed_statement)

        # Write the modified code to a new file
        with open(test_file[:-9] + "final.py", 'w') as output_file:
            output_file.write(astunparse.unparse(tree))

    def execute_test(self, file_name, test_name):
        spec = importlib.util.spec_from_file_location(test_name, file_name)
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)

        test_function = getattr(test_module.Tests, test_name, None)
        if test_function is not None and callable(test_function):
            test_instance = test_module.Tests()
            test_function(test_instance)
        else:
            print(f"Error: Test function '{test_name}' not found in module '{file_name}'.")

if __name__ == "__main__":
    instrumentor = Inst()
    instrumentor.instrument_assertion("task3results/assertions_logged.py", "test_func")
    instrumentor.execute_test("task3results/assertions_logged.py", "test_func")
