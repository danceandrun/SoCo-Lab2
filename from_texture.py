import sys
import json


def do_addieren(envs_stack, args):
    """Handles the 'addieren' operation; e.g., ["addieren",1,2]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of the two values to add
        (they can be other operations)

    Returns
    -------
    int
        the sum of the two values
    """

    assert len(args) == 2
    left = do(envs_stack, args[0])
    right = do(envs_stack, args[1])
    return left + right


def do_betrag(envs_stack, args):
    """Handles the 'betrag' operation; e.g., ["betrag",-1]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : object
        The value for which to compute
        the absolute number

    Returns
    -------
    int
        the absolute number the value
    """

    assert len(args) == 1
    val = do(envs_stack, args[0])
    return abs(val)


def do_sequenz(envs_stack, args):
    """Handles the 'sequenz' operation

    Example:
    ["sequenz",
        ["setzen", "alpha", 1],
        ["bekommen", "alpha"]
    ]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    args : list
        The list of operations to execute

    Returns
    -------
    int
        the return value of the last operation
        in the list of args
    """

    assert len(args) > 0
    result = None
    for expr in args:
        result = do(envs_stack, expr)
    return result


def do_setzen(envs_stack, args):
    """Handles the 'setzen' operation; e.g., ["setzen", "alpha", 1]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
        where to store/update the variable
    args : list
        args[0] : name of variable
        args[1] : content of variable

    Returns
    -------
    int
        the value associated to the var
    """

    assert len(args) == 2
    assert isinstance(args[0], str)
    var_name = args[0]
    value = do(envs_stack, args[1])
    # previous version:
    # env[var_name] = value
    # new version with stack of environments
    set_in_envs_stack(envs_stack, var_name, value)
    return value


def do_bekommen(envs_stack, args):
    """Handles the 'bekommen' operation; e.g., ["bekommen", "alpha"]

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
        from which to retrieve the variable
    args : str
        The name of the variable

    Returns
    -------
    object
        the content of the variable
    """

    assert len(args) == 1
    assert isinstance(args[0], str)
    # code below is no longer necessary
    # because the check is done by the function
    # get_from_envs_stack we call later
    # assert args[0] in envs_stack, f"Variable name {args[0]} not found"
    # previous version:
    # value = env[args[0]]
    # new version
    value = get_from_envs_stack(envs_stack, args[0])
    return value


def do_func(envs_stack, args):
    """Handles the 'func' operation; ["func", "n", ["bekommen","n"]]

    This function does not do much: it only
    prepares the data structure to store in
    memory, which can then be called later

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
        (only here for consistency)
    args : list
        args[0] : parameters of the function
        args[1] : body of the function

    Returns
    -------
    list
        the list with parameters and body
    """

    assert len(args) == 2
    parameters = args[0]
    body = args[1]
    return ["func", parameters, body]


def do_call(envs_stack, args):
    """Handles the 'call' operation; e.g., ["call","add_two",3,2]

    where "add_two" is the name of a function
    previously defined, and the rest are the
    arguments to pass to the function

    Parameters
    ----------
    envs_stack : list
        The stack with the environments,
        to which it pushes the specific env
        for the function when called and
        pop it afterwards
    args : list
        args[0] : name of function to call
        args[1] : arguments to pass to func

    Returns
    -------
    object
        the return value of the body execution
    """

    # setting up the call
    assert len(args) >= 1
    assert isinstance(args[0], str)
    func_name = args[0]  # "add_two"
    arguments = [do(envs_stack, a) for a in args[1:]]  # [3, 2]

    # find the function
    func = get_from_envs_stack(envs_stack, func_name)
    assert isinstance(func, list) and func[0] == "func", \
        f"{func_name} is not a function!"
    params = func[1]  # ["num1","num2"]
    body = func[2]  # ["addieren","num1","num2"]
    assert len(arguments) == len(params), \
        f"{func_name} receives a different number of parameters"
    # create the env for the function
    # params = ["num1","num2"], values = [3, 2]
    # env = {"num1":3, "num2":2}
    local_env = dict(zip(params, arguments))

    # push new env into the stack
    envs_stack.append(local_env)
    result = do(envs_stack, body)
    envs_stack.pop()

    return result


def set_in_envs_stack(envs_stack, name, value):
    """Adds a variable and its value to the environment stack

    if the variable name has already been defined in the stack of
    environments, it updates the value.
    Otherwise, it creates a new variable in the top environment.

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    name : str
        name of the fuction to set
    value : object
        value to associate to the variable

    Returns
    -------
    None
        nothing is returned, could have returned the set value
    """

    assert isinstance(name, str)
    for each_env in reversed(envs_stack):
        if name in each_env:
            # update the found variable
            each_env[name] = value
            # and exit
            return
    # otherwise add it to the
    # last inserted environment
    top_environment = envs_stack[-1]
    top_environment[name] = value


def get_from_envs_stack(envs_stack, name):
    """Gets the value of a variable from the environment stack

    It uses dynamic scoping: it visits the entire environment stack,
    from the latest inserted environment to the first, to find the
    variable name.

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    name : str
        name of the value to search

    Returns
    -------
    object
        value to associate to the variable
    """

    assert isinstance(name, str)
    for each_env in reversed(envs_stack):
        if name in each_env:
            return each_env[name]
    assert False, f"Name {name} not found"


def do(envs_stack, expr):
    """Executes the given expression

    Our minimal operation is an integer value; everything else is
    then computed to a value.

    Parameters
    ----------
    envs_stack : list
        The stack with the environments
    operation : object
        operation to be executed

    Returns
    -------
    object
        value of the computed operation
    """

    if isinstance(expr, int):
        return expr
    assert isinstance(expr, list)
    assert expr[0] in OPS, f"Unknown operation {expr[0]}"
    operation = OPS[expr[0]]
    return operation(envs_stack, expr[1:])


# dynamically find and name all operations we support in our language
OPS = {
    name.replace("do_", ""): func
    for (name, func) in globals().items()
    if name.startswith("do_")
}


def main():
    """Executes the interpreter on the given code file.

    The function also creates the global environment and the stack of
    enviroments, which will be then passed around. It prints the result
    of the computation.

    """
    program = ""
    assert len(sys.argv) == 2, "usage: python interpreter.py code.tll"
    with open(sys.argv[1], "r") as source:
        program = json.load(source)
    # old version:
    # result = do({}, program)
    # new version with stack of envs
    envs_stack = []  # to be filled with envs
    global_environment = {}  # first environment we use
    envs_stack.append(global_environment)  # push it to the stack
    result = do(envs_stack, program)
    print(result)


if __name__ == "__main__":
    main()
