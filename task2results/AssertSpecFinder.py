import os
import ast
import csv
import astunparse

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
                        if self.is_approx_assertion(statement):
                            assertion_string = astunparse.unparse(statement).strip()
                            self.assertions.append({
                                'filepath': filepath,
                                'testclass': node.name if hasattr(node, 'name') else '',
                                'testname': node.name,
                                'assertion type': 'approximate',
                                'line number': statement.lineno,
                                'assert string': assertion_string
                            })

    def is_approx_assertion(self, assert_node):
        if isinstance(assert_node, ast.Assert):
            if isinstance(assert_node.test, ast.Compare):
                for op in assert_node.test.ops:
                    if not isinstance(op, ast.Eq): 
                        return True
        
        if isinstance(assert_node, ast.Expr):
            if isinstance(assert_node.value, ast.Call):
                call_node = assert_node.value
                if isinstance(call_node.func, ast.Attribute):
                    attr_node = call_node.func
                    if isinstance(attr_node.value, ast.Name) and attr_node.value.id == 'self':
                        if isinstance(attr_node.attr, str) and attr_node.attr.startswith('assert'):
                            return True
        return False


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

if __name__ == "__main__":
    finder = AssertSpecFinder("qiskit")
    finder.find_assertions("task2results/qiskit-aqua-main/test/")
    finder.output_to_csv()

    finder = AssertSpecFinder("tensorflow")
    finder.find_assertions("task2results/tensor2tensor-master/")
    finder.output_to_csv()

    finder = AssertSpecFinder("pytorch")
    finder.find_assertions("task2results/vision-main/test")
    finder.output_to_csv()
