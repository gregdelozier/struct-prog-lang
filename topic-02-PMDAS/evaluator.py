from tokenizer import tokenize
from parser import parse

printed_string = None

def evaluate(ast):
    global printed_string
    if ast["tag"] == "print":
        value = evaluate(ast["value"])
        s = str(value)
        print(s)
        printed_string = s
        return None
    if ast["tag"] == "number":
        return ast["value"]
    if ast["tag"] in ["+","-","*","/"]:
        left_value = evaluate(ast["left"])
        right_value = evaluate(ast["right"])
        if ast["tag"] == "+":
            return left_value + right_value
        if ast["tag"] == "-":
            return left_value - right_value
        if ast["tag"] == "*":
            return left_value * right_value
        if ast["tag"] == "/":
            return left_value / right_value

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

def eval(s):
    tokens = tokenize(s)
    ast = parse(tokens)
    result = evaluate(ast)
    return result

def test_evaluate_expression():
    print("testing evaluate expression")
    assert eval("1+2+3") == 6
    assert eval("1+2*3") == 7
    assert eval("(1+2)*3") == 9
    assert eval("(1.0+2.1)*3") == 9.3

def test_evaluate_print():
    print("testing evaluate print")
    assert eval("print 3") == None    
    assert printed_string == "3"
    assert eval("print 3.14") == None    
    assert printed_string == "3.14"

if __name__ == "__main__":
    test_evaluate_number()
    test_evaluate_addition()
    test_evaluate_subtraction()
    test_evaluate_multiplication()
    test_evaluate_division()
    test_evaluate_expression()
    test_evaluate_print()
    print("done.")