To run the AssertSpecFinder program on a given Python project, you will need
either the relative or absolute path of the directory you would like to search
for tests as well as a name for the prefix of the output csv file. 

The general code to generate a full report of assertions is as follows: 

'''
import AssertSpecFinder

finder = AssertSpecFinder("csv_name_prefix")
finder.run("path_to_project")
'''

For example, to generate the assertions in qiskit-aqua, it would be the 
following, assuming your relative path aligns with my directory structure: 

'''
import AssertSpecFinder

finder = AssertSpecFinder("qiskit")
finder.run("task2results/qiskit-aqua-main/")
'''