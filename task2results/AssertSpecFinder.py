import os
import ast
import csv
import astunparse

class AssertSpecFinder:
    def __init__(self, project_name):
        self.project_name = project_name
        self.assertions = []

    def analyze_file(self, filepath):
        print("Checkpoint 1")
        with open(filepath, 'r') as file:
            print("Checkpoint 2")
            tree = ast.parse(file.read())
            for node in ast.walk(tree):
                print("Checkpoint 3")
                if isinstance(node, ast.FunctionDef):
                    print("Checkpoint 4")
                    for statement in node.body:
                        print("Checkpoint 5")
                        if isinstance(statement, ast.Assert):
                            print("Checkpoint 6")
                            if self.is_approx_assertion(statement):
                                print("Checkpoint 7")
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
        print("Checkpoint 1")
        if isinstance(assert_node.test, ast.Call):
            print("Checkpoint 2")
            if isinstance(assert_node.test.func, ast.Attribute):
                print("Checkpoint 3")
                if isinstance(assert_node.test.func.value, ast.Name) and assert_node.test.func.value.id == 'self':
                    print("Checkpoint 4")
                    if isinstance(assert_node.test.func.attr, str) and assert_node.test.func.attr == 'assertTrue':
                        print("Checkpoint 5")
                        return True
        return True

    def find_assertions(self, directory):
        if not os.path.isdir(directory):
            print(f"Error: '{directory}' is not a valid directory.")
            return
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
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
    finder = AssertSpecFinder("example")
    finder.find_assertions("task2results/qiskit-aqua-main/test/aqua/")

    finder.output_to_csv()
