import importlib.util
import ast
import astunparse

class Inst:
    def detect_alias(self, tree, module_name):
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == module_name:
                        if alias.asname:
                            return alias.asname

        return module_name

    def is_assignment(self, stmt):
        if isinstance(stmt, ast.Assign):
            if isinstance(stmt.value, ast.Call):
                if isinstance(stmt.value.func, ast.Attribute):
                    return True
        
        return False

    def numpy_used(self, stmt, alias, library):
        if self.is_assignment(stmt):
            if isinstance(stmt.value.func.value, ast.Attribute):
                if stmt.value.func.value.attr == library:
                    if isinstance(stmt.value.func.value.value, ast.Name):
                        if stmt.value.func.value.value.id == alias:
                            return True
                            
        return False
    
    def tensorflow_used(self, stmt, alias, library):
        if self.is_assignment(stmt):
            if isinstance(stmt.value.func.value, ast.Attribute):
                if stmt.value.func.value.attr == library:
                    if isinstance(stmt.value.func.value.value, ast.Name):
                        if stmt.value.func.value.value.id == alias:
                            return True
                            
        return False

    def pytorch_used(self, stmt, alias, library):
        if self.is_assignment(stmt):
            if stmt.value.func.attr[:4] == library:
                if isinstance(stmt.value.func.value, ast.Name):
                    if stmt.value.func.value.id == alias:
                        return True

        return False

    def random_used(self, stmt, alias, library):
        if self.is_assignment(stmt):
            if isinstance(stmt.value.func.value, ast.Name):
                if stmt.value.func.value.id == alias:
                    return True

        return False

    
    def find_parent_block(self, tree, node):
        """
        Find the parent block of a given node in the AST tree.
        """
        for item in ast.walk(tree):
            if isinstance(item, ast.FunctionDef) and node in item.body:
                return item
            elif isinstance(item, ast.ClassDef) and node in item.body:
                return item
            elif isinstance(item, ast.Module) and node in item.body:
                return item
        
        parent_block = None
        for item in ast.walk(tree):
            if isinstance(item, (ast.FunctionDef, ast.ClassDef)) and node in item.body:
                parent_block = item
            elif isinstance(item, ast.Import) or isinstance(item, ast.ImportFrom):
                break
        return parent_block

    def instrument_assertion(self, test_file, test_name):
        with open(test_file, 'r') as file:
            tree = ast.parse(file.read())

        test_function = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == test_name:
                test_function = node
                break

        if test_function:
            #Numpy random.seed
            #TensorFlow random.set_seed
            #PyTorch manual_seed
            #Random (Python) seed
            random_used = [False, False, False, False]
            seeds = [42, 42, 42, 42]
            aliases = ["numpy", "tensorflow", "torch", "random"]
            random_lib = ["random", "random", "rand", ""]
            seed_setter = ["seed", "set_seed", "manual_seed", "seed"]
            usage_tester = [self.numpy_used, self.tensorflow_used, 
                    self.pytorch_used, self.random_used]

            for i in range(len(aliases)):
                aliases[i] = self.detect_alias(tree, aliases[i])

            for statement in test_function.body:
                for i in range(len(random_used)):
                    if random_used[i]:
                        continue

                    if (usage_tester[i](statement, aliases[i], random_lib[i])):
                        random_used[i] = True

            for i in range(len(random_used)):
                if random_used[i]:
                    value = ast.Attribute(
                        value=ast.Name(id=aliases[i], ctx=ast.Load()),
                        attr='random',
                        ctx=ast.Load()
                    )

                    if i == 2 or i == 3:
                        value = ast.Name(id=aliases[i], ctx=ast.Load())
                    
                    seed_statement = ast.Expr(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=value,
                                attr=seed_setter[i],
                                ctx=ast.Load()
                            ),
                            args=[ast.Constant(value=seeds[i], kind=None)],
                            keywords=[]
                        )
                    )
                    
                    (self.find_parent_block(tree, test_function)).body.insert(0, seed_statement)

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
