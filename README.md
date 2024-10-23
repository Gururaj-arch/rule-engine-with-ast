# rule-engine-with-ast
This project implements an Abstract Syntax Tree (AST) for evaluating user-defined rules based on given data. The primary focus is on parsing rules in a string format, constructing an AST representation, and evaluating conditions without using eval, ensuring a secure and robust implementation.
Features
AST Construction: Parse rule strings with logical operators (AND, OR) and conditions (comparisons such as >, <, and =) to build an AST.
Rule Evaluation: Recursively evaluate the AST against user data to determine whether the conditions are met.
Custom Error Handling: Implement custom exceptions for invalid rules and missing data, providing clear feedback on issues during parsing or evaluation.
Test Cases: Includes comprehensive test cases to validate both valid and invalid rule strings, as well as edge cases related to data completeness.
Installation
To use this project, you can clone the repository and run the Python script directly. Ensure you have Python installed on your machine.
Usage
Define your rule string, such as "age > 30 AND department = 'Sales'".
Use the create_rule function to generate an AST.
Prepare user data in dictionary format (e.g., {'age': 35, 'department': 'Sales'}).
Call the evaluate_rule function with the AST and the user data to check if the conditions are satisfied.
