import re

# Define the Node class for AST representation
class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type  # 'operator' or 'operand'
        self.value = value          # Value for operand nodes (e.g., age > 30)
        self.left = left            # Left child node
        self.right = right          # Right child node

    def __repr__(self):
        return f"Node({self.node_type}, {self.value}, {self.left}, {self.right})"


# Custom exception for invalid rules
class InvalidRuleException(Exception):
    """Custom exception for invalid rules."""
    pass


# Function to create an AST from a rule string
def create_rule(rule_string):
    # Split rule string by AND/OR operators
    tokens = re.split(r'(\sAND\s|\sOR\s)', rule_string)

    # Parse conditions like 'age > 30', 'department = "Sales"', etc.
    def parse_condition(condition):
        if '>' in condition:
            left, right = condition.split('>')
            return Node('operand', (left.strip(), '>', right.strip()))
        elif '<' in condition:
            left, right = condition.split('<')
            return Node('operand', (left.strip(), '<', right.strip()))
        elif '=' in condition:
            left, right = condition.split('=')
            # Remove quotes around string values
            right_value = right.strip().replace("'", "").replace('"', "")
            return Node('operand', (left.strip(), '==', right_value))
        else:
            raise InvalidRuleException(f"Invalid condition: {condition}")

    root = None
    operator_node = None

    for token in tokens:
        token = token.strip()
        if token in ['AND', 'OR']:
            operator_node = Node('operator', token)
        else:
            condition_node = parse_condition(token)
            if root is None:
                root = condition_node
            else:
                if operator_node is None:
                    raise InvalidRuleException("No operator between conditions")
                operator_node.left = root
                operator_node.right = condition_node
                root = operator_node

    if root is None:
        raise InvalidRuleException("Invalid rule string provided")
    
    return root


# Function to combine multiple rules into one AST
def combine_rules(rules):
    root = None

    for rule in rules:
        rule_ast = create_rule(rule)
        if root is None:
            root = rule_ast
        else:
            # Combine current AST with new rule using AND (or modify to OR as needed)
            root = Node('operator', 'AND', root, rule_ast)

    return root


# Function to evaluate an AST against a user's data without using eval
def evaluate_rule(ast, data):
    try:
        if ast.node_type == 'operand':
            # Extract the condition parts
            left, operator, right = ast.value

            # Get the value from the user's data for the left side
            if left not in data:
                raise ValueError(f"Missing data for: {left}")

            left_value = data[left]
            print(f"Evaluating: {left_value} {operator} {right}")  # Debugging print

            # Perform the appropriate comparison
            if operator == '>':
                result = float(left_value) > float(right)
                print(f"Comparison result: {result}")  # Debugging print
                return result
            elif operator == '<':
                result = float(left_value) < float(right)
                print(f"Comparison result: {result}")  # Debugging print
                return result
            elif operator == '==':
                # Ensure string comparison by casting both to strings
                result = str(left_value).lower() == right.lower()
                print(f"Comparison result: {result}")  # Debugging print
                return result

        elif ast.node_type == 'operator':
            left_result = evaluate_rule(ast.left, data)
            print(f"Left Result: {left_result}")  # Debugging print
            right_result = evaluate_rule(ast.right, data)
            print(f"Right Result: {right_result}")  # Debugging print

            if ast.value == 'AND':
                return left_result and right_result
            elif ast.value == 'OR':
                return left_result or right_result

        return False

    except Exception as e:
        raise ValueError(f"Error while evaluating rule: {e}")

# Test Cases for Valid Rules and Data
def test_valid_cases():
    print("Test Case 1 Starting...")

    # Rule 1: Only this rule should be evaluated in Test Case 1
    rule1 = "age > 30 AND department = 'Sales'"
    
    # Combine rules (single rule for this test case)
    rule1_ast = create_rule(rule1)

    # Test case 1: User matches the first rule
    user_data_1 = {
        'age': 35,
        'department': 'Sales',
        'salary': 60000,
        'experience': 5
    }
    result_1 = evaluate_rule(rule1_ast, user_data_1)
    print(f"Test Case 1 Result: {result_1}")  # Debugging print
    assert result_1 == True, "Test Case 1 Failed"

    # Now evaluate the second rule separately (Test Case 2)
    print("Test Case 2 Starting...")
    rule2 = "age < 25 AND department = 'Marketing'"
    rule2_ast = create_rule(rule2)

    # Test case 2: User does not match the second rule
    user_data_2 = {
        'age': 28,
        'department': 'Engineering',
        'salary': 70000,
        'experience': 4
    }
    result_2 = evaluate_rule(rule2_ast, user_data_2)
    print(f"Test Case 2 Result: {result_2}")  # Debugging print
    assert result_2 == False, "Test Case 2 Failed"

    print("All valid test cases passed!")


# Test Cases for Invalid Rules and Data
def test_invalid_cases():
    print("Test Case for Invalid Rule Starting...")

    # Invalid rule string (no operator between conditions)
    invalid_rule = "age > 30 department = 'Sales'"
    try:
        create_rule(invalid_rule)
    except InvalidRuleException:
        print("Caught invalid rule as expected")

    # Test evaluation with missing data
    print("Test Case for Missing Data Starting...")
    rule = "age > 30 AND salary > 50000"
    rule_ast = create_rule(rule)

    # Missing 'salary' in the data
    incomplete_data = {
        'age': 35,
        'department': 'Sales'
    }

    try:
        result = evaluate_rule(rule_ast, incomplete_data)
    except ValueError:
        print("Caught error due to missing data as expected")


if __name__ == "__main__":
    print("Running valid test cases...")
    test_valid_cases()

    print("Running invalid test cases...")
    test_invalid_cases()
