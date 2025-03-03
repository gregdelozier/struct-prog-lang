from tokenizer import tokenize
from parser import parse

printed_string = None

def evaluate(ast, environment={}):
    global printed_string
    if ast["tag"] == "program":
        last_value = None
        for statement in ast["statements"]:
            value = evaluate(statement, environment)
            last_value = value
        return last_value
    if ast["tag"] == "print":
        value = evaluate(ast["value"])
        s = str(value)
        print(s)
        printed_string = s
        return None
    if ast["tag"] == "assign":
        target = ast["target"]
        assert target["tag"] == "identifier"
        identifier = target["value"]
        assert type(identifier) is str
        value = evaluate(ast["value"],environment)
        environment[identifier] = value
    if ast["tag"] == "number":
        return ast["value"]
    if ast["tag"] == "identifier":
        if ast["value"] in environment:
            return environment[ast["value"]]
        parent_environment = environment
        while "$parent" in parent_environment:
            parent_environment = environment["$parent"]
            if ast["value"] in parent_environment:
                return parent_environment[ast["value"]]
        raise Exception(f"Value [{ast["value"]}] not found in environment {environment}.")
    if ast["tag"] in ["+", "-", "*", "/"]:
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        if ast["tag"] == "+":
            return left_value + right_value
        if ast["tag"] == "-":
            return left_value - right_value
        if ast["tag"] == "*":
            return left_value * right_value
        if ast["tag"] == "/":
            return left_value / right_value
    if ast["tag"] == "negate":
        value = evaluate(ast["value"], environment)
        return -value
    if ast["tag"] == "&&":
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        return left_value and right_value
    if ast["tag"] == "||":
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        return left_value or right_value
    if ast["tag"] == "!":
        value = evaluate(ast["value"], environment)
        return not value
    if ast["tag"] == "<":
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        return left_value < right_value
    if ast["tag"] == ">":
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        return left_value > right_value
    if ast["tag"] == "<=":
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        return left_value <= right_value
    if ast["tag"] == ">=":
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        return left_value >= right_value
    if ast["tag"] == "==":
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        return left_value == right_value
    if ast["tag"] == "!=":
        left_value = evaluate(ast["left"], environment)
        right_value = evaluate(ast["right"], environment)
        return left_value != right_value


def test_evaluate_number():
    print("testing evaluate number")
    assert evaluate({"tag":"number","value":4}) == 4

def test_evaluate_addition():
    print("testing evaluate addition")
    ast = {
        "tag":"+",
        "left":{"tag":"number","value":1},
        "right":{"tag":"number","value":3}
        }
    assert evaluate(ast) == 4

def test_evaluate_subtraction():
    print("testing evaluate subtraction")
    ast = {
        "tag":"-",
        "left":{"tag":"number","value":3},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast) == 1

def test_evaluate_multiplication():
    print("testing evaluate multiplication")
    ast = {
        "tag":"*",
        "left":{"tag":"number","value":3},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast) == 6

def test_evaluate_division():
    print("testing evaluate division")
    ast = {
        "tag":"/",
        "left":{"tag":"number","value":4},
        "right":{"tag":"number","value":2}
        }
    assert evaluate(ast) == 2

def eval(s, environment={}):
    tokens = tokenize(s)
    ast = parse(tokens)
    result = evaluate(ast, environment)
    return result

def test_evaluate_expression():
    print("testing evaluate expression")
    assert eval("1+2+3") == 6
    assert eval("1+2*3") == 7
    assert eval("(1+2)*3") == 9
    assert eval("(1.0+2.1)*3") == 9.3
    assert eval("1<2") == True
    assert eval("2<1") == False
    assert eval("2>1") == True
    assert eval("1>2") == False
    assert eval("1<=2") == True
    assert eval("2<=2") == True
    assert eval("2<=1") == False
    assert eval("2>=1") == True
    assert eval("2>=2") == True
    assert eval("1>=2") == False
    assert eval("2==2") == True
    assert eval("1==2") == False
    assert eval("2!=1") == True
    assert eval("1!=1") == False
    # tokens = tokenize("-1")
    # ast = parse(tokens)
    # result = evaluate(ast, {})
    # print(ast, result)
    # exit(0)

    assert eval("-1") == -1
    assert eval("-(1)") == -1
    assert eval("!1") == False
    assert eval("!0") == True
    assert eval("0&&1") == False
    assert eval("1&&1") == True
    assert eval("1||1") == True
    assert eval("0||1") == True
    assert eval("0||0") == False


def test_evaluate_identifier():
    print("testing evaluate identifier")
    try:
        assert eval("x+3") == 6
        raise Exception("Error expected for missing value in environment")
    except Exception as e:
        assert "not found" in str(e) 
    assert eval("x+3", {"x":3}) == 6
    assert eval("x+y",{"x":4,"y":5}) == 9
    assert eval("x+y",{"$parent":{"x":4},"y":5}) == 9

def test_evaluate_print():
    print("testing evaluate print")
    assert eval("print 3") == None    
    assert printed_string == "3"
    assert eval("print 3.14") == None    
    assert printed_string == "3.14"

def test_evaluate_assignment():
    print("testing evaluate assignment")
    env = {"x":4,"y":5}
    assert eval("x=7",env) == 7
    assert env["x"] == 7

if __name__ == "__main__":
    test_evaluate_number()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_expression()
    test_evaluate_print()
    test_evaluate_identifier()
    print("done.")
