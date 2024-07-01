# Flaky Test Experience

## How to Use

### Task 1 Results

This section has no code. 

### Task 2 Results

Place a python project in the task2results directory, then run AssertSpecFinder.py. 

Set the names of the target directory and result csv name as follows:
```
finder = AssertSpecFinder(result_name)
finder.run("task2results/target_project/")
```

For example,
```
finder = AssertSpecFinder("qiskit")
finder.run("task2results/qiskit-aqua-main/")
```
reads the `qiskit-aqua-main` folder and writes assertions to `qiskit_assertions.csv`.

This tool will log all potentially flaky assertions, for example `assert 5.0 == 5.0`.

### Task 3 Results

Place a python file (or folder with a file) in the task3results directory, then run instrumentor.py.

Specify the path to the file, function inside the file, and line of the function as follows:
```
instrumentor = Instrumentor()
instrumentor.instrument_assertion("task3results/file_name.py", "function_name", line_number)
```

For example, 
```
instrumentor = Instrumentor()
instrumentor.instrument_assertion("task3results/assertions.py", "test_func", 10)
```
will log the `assert (x < y)` assertion in the `test_func` function in `assertions.py`.

The logging portion of this tool will log potentially flaky assertions, the main difference is that the logging is in code, exposing variable values. 

The logged file is an intermediate, suffixed with `_logged`.

The second step is to seed any randomness to reduce flakiness in the files. Currently, only numpy.random is seeded, but this can be easily extended to other randomness generators. 

After this step, the final file is produces, suffixed with `_final`.

## Project Structure

**flaky-test-exp/**
  - **task1results/**
    - report1.txt  
    - review-fse14.txt  
    - review-issta20.txt 
  - **task2results/**
    - **qiskit-aqua-main/**  
      - Internal structure   
    - **tensor2tensor-master/**    
      - Internal structure
    - **vision-main/**   
      - Internal structure
    - AssertSpecFinder.py   
    - pytorch_assertions.csv
    - qiskit_assertions.csv  
    - tensorflow_assertions.csv  
    - README.md  
    - report1.txt
  - **task3results/**
    - assertions_logged.py   
    - assertions_final.py    
    - assertions.py   
    - instrumentor.py
    - report2.txt   
    - script.py   
    - t1.py  
    - t2.py
  - **.gitignore**
  - **README.MD**
  - **report.txt**