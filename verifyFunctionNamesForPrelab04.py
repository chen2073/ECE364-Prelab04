#! /user/local/bin/python3.4

from inspect import getmembers, isfunction

# Define desired functions that should be present.
functionNames = ['get_circuit_by_student', 'get_circuit_by_student_partial', 'get_common_by_project', 'get_common_by_student',
                 'get_component_by_student', 'get_component_count_by_project', 'get_component_count_by_student',
                 'get_participation_by_project', 'get_participation_by_student', 'get_project_by_circuit',
                 'get_project_by_component', 'get_student_by_component']

# Attempt to import the code, and fail otherwise.
try:
    import project_analytics as student
except:
    print("-------------------------------")
    print("Unable to find expected file.")
    print("-------------------------------")
    print()
    exit(-1)
else:
    print("-------------------------------")
    print("Code file imported successfully.")
    print("-------------------------------")
    print()

# Obtain all functions in the code.
presentFunctions = [fnName for fnName, _ in getmembers(student, isfunction)]

# Check whether each function is present or missing, and print out the result.
for fnIndex, fnName in enumerate(functionNames):

    if fnName in presentFunctions:
        print('{:02d}- Function "{}" located.'.format(fnIndex + 1, fnName))
    else:
        print('{:02d}- =======> Unable to locate the function "{}".'.format(fnIndex + 1, fnName))
