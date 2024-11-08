import sys
import json

# Infix arithmetic operations
def infix_evaluator(infix_expression : str) -> int :
    token_list = infix_expression.split()
    # print(token_list)
    # The dictionary of the operators precedence
    pre_dict = {'*' : 3, '/' : 3, '+' : 2, '-' : 2, 
                'AND' : 1, 'OR' : 1, 'XOR' : 1,
                '(' : 0
               }
    # The operators' stack
    operator_stack = []
    # The numbers' stack
    operand_stack = []

    for token in token_list:
        # Numbers pushed into the stack
        if token.isdecimal() or (token[1:].isdecimal() and token[0] == '-'):
            operand_stack.append(int(token))
        
        # Left bracket into the operators' stack
        elif token == '(':
            operator_stack.append(token)
        
        # When a right bracket is encountered, all operators on top of the left bracket in the stack should be popped.
        elif token == ')':
            top = operator_stack.pop()
            while top != '(':
                # Every operator is popped, then two numbers should be popped to calculate.
                # Note: the order of popping operands is reversed. The number that pops out first is op2.
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                # The calculation result should be pushed into the numbers' stack
                operand_stack.append(get_value(top, op1, op2))
                # Pop the next operator on the top of the stack
                top = operator_stack.pop()

        # When an operator is encountered, all operators on top of the stack with a priority not lower than it must be popped out for evaluation.
        elif token in pre_dict:
            while operator_stack and pre_dict[operator_stack[-1]] >= pre_dict[token]:
                top = operator_stack.pop()
                op2 = operand_stack.pop()
                op1 = operand_stack.pop()
                operand_stack.append(get_value(top, op1, op2))
            # The current operator should be pushed into the stack
            operator_stack.append(token)

    # After the expression traversal is completed, the remaining operators on the stack also require calcualtion.  
    while operator_stack:
        top = operator_stack.pop()
        op2 = operand_stack.pop()
        op1 = operand_stack.pop()
        operand_stack.append(get_value(top, op1, op2))
    # There is only one number left on the stack in the end, and this number is the final result of the entire expression.
    return operand_stack[0]

def get_value(operator : str, op1 : int, op2 : int):
    if operator == '+':
        return op1 + op2
    elif operator == '-':
        return op1 - op2
    elif operator == '*':
        return op1 * op2
    elif operator == '/':
        return op1 / op2
    elif operator == 'AND':
        # return 1 if op1 == 1 and op2 == 1 else 0
        return op1 and op2
    elif operator == 'OR':
        # return 0 if op1 == 0 or op2 == 0 else 1
        return  op1 or op2
    elif operator == 'XOR':
        return 1 if (op1 == 1) != (op2 == 1) else 0
    else:
        raise ValueError(f"Unsupported operator: {operator}")

# Execute the given program expression
def do(envs_stack, expr):
    if isinstance(expr, int):
        return expr
    elif isinstance(expr, str):  # Support direct infix string evaluation
        return infix_evaluator(expr)
    elif isinstance(expr, list) and expr[0] in OPS:
        operation = OPS[expr[0]]
        return operation(envs_stack, expr[1:])
    else:
        raise ValueError("Unknown expression format")

# Environment operations
def do_sequenz(envs_stack, args):
    results = []
    for expr in args:
        result = do(envs_stack, expr)
        results.append(result)
    return results

def do_setzen(envs_stack, args):
    var_name = args[0]
    value = do(envs_stack, args[1])
    envs_stack[-1][var_name] = value
    return value

def do_bekommen(envs_stack, args):
    var_name = args[0]
    return envs_stack[-1][var_name]

# Supported operations
OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}

# Executes the interpreter on the given code file
def main():
    assert len(sys.argv) == 2, "Usage: python lgl_interpreter.py example_infix.gsc"
    file_path = sys.argv[1]
    
    # Load program from the given JSON file
    with open(file_path, "r") as source:
        program = json.load(source)
    
    envs_stack = [{}]  # Initialize environment stack
    result = do(envs_stack, program)
    
    print("Results for each expression in sequence:")
    for i, result in enumerate(result, start = 1):
        print(f"Expression {i}: {result}")

# if __name__ == "__main__":
#     main()

def test_Feniel():
    # Load program from the given JSON file
    with open('example_infix.gsc', "r") as source:
        program = json.load(source)

    envs_stack = [{}]  # Initialize environment stack
    result = do(envs_stack, program)

    print("Results for each expression in sequence:")
    for i, result in enumerate(result, start=1):
        print(f"Expression {i}: {result}")

test_Feniel()