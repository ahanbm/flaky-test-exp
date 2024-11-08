import os
import ast
import csv

class AssertSpecFinder:
    def __init__(self, project_name):
        self.project_name = project_name
        self.assertions = []

    def analyze_file(self, filepath):
        with open(filepath, 'r') as file:
            tree = ast.parse(file.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    for statement in node.body:
                        assert_type = self.is_approx_assertion(statement)
                        if self.is_valid(assert_type):
                            if (assert_type == "assertEqual"):
                                print(self.is_valid("assertEqual"))

                            assertion_string = ast.unparse(statement).strip()
                            self.assertions.append({
                                'filepath': filepath,
                                'testclass': node.name if hasattr(node, 'name') else '',
                                'testname': node.name,
                                'assertion type': assert_type,
                                'line number': statement.lineno,
                                'assert string': assertion_string
                            })

    def is_valid(self, assert_type):
        if not assert_type:
            return False

        return (
            assert_type == "assert expr < | > | <= | >= threshold" or
            assert_type == "assertTrue" or
            assert_type == "assertFalse" or
            assert_type == "assert_almost_equal" or
            assert_type == "assertGreater" or
            assert_type == "assertGreaterEqual" or
            assert_type == "assertLess" or
            assert_type == "assertLessEqual" or
            assert_type == "assertNotAlmostEqual" or
            assert_type == "assertNotEqual" or
            assert_type == "assertNotRegex" or
            assert_type == "assertRegex" or
            assert_type == "assertApproxRegex" or
            assert_type == "assert_approx_equal" or
            assert_type == "assert_array_almost_equal" or
            assert_type == "assert_all_close" or
            assert_type == "assert_array_less" or
            assert_type == "assertAllClose"
        )

    def is_approx_assertion(self, assert_node):
        if isinstance(assert_node, ast.Assert):
            if isinstance(assert_node.test, ast.Compare):
                for op in assert_node.test.ops:
                    if (
                        isinstance(op, ast.Lt) or 
                        isinstance(op, ast.Gt) or 
                        isinstance(op, ast.LtE) or 
                        isinstance(op, ast.GtE)
                    ): 
                        return "assert expr < | > | <= | >= threshold"
        
        if isinstance(assert_node, ast.Expr):
            if isinstance(assert_node.value, ast.Call):
                call_node = assert_node.value
                if isinstance(call_node.func, ast.Attribute):
                    attr_node = call_node.func
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


    def find_assertions(self, directory):
        if not os.path.isdir(directory):
            print(f"Error: '{directory}' is not a valid directory.")
            return
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.startswith('test') and file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    if not os.path.isfile(file_path):
                        print(f"Warning: '{file_path}' is not a regular file.")
                        continue
                    self.analyze_file(file_path)

    def output_to_csv(self):
        csv_filename = f"task2results/{self.project_name}_assertions.csv"
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = ['filepath', 'testclass', 'testname', 'assertion type', 'line number', 'assert string']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for assertion_data in self.assertions:
                writer.writerow(assertion_data)

    def run(self, library):
        self.find_assertions(library)
        self.output_to_csv()

if __name__ == "__main__":
    finder = AssertSpecFinder("qiskit")
    finder.run("task2results/qiskit-aqua-main/")

    finder = AssertSpecFinder("tensorflow")
    finder.run("task2results/tensor2tensor-master/")

    finder = AssertSpecFinder("pytorch")
    finder.run("task2results/vision-main/")
