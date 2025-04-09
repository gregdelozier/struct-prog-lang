#!/usr/bin/env python
from tokenizer import tokenize

"""
parser.py
"""

# Grammar 
grammar = """
    parameters = "(" [ identifier { "," identifier } ] ")"
    arguments = "(" [ expression { "," expression } ] ")"
    block = "{" statement { ";" statement } "}"
    array = "[" [ expression { "," expression } ] "]"
    object = "{" [ (string | identifier) ":" expression { "," (string | identifier) ":" expression } ] "}"
    function = "function" parameters block
    simple_expression = <number> | <string> | <identifier> | "(" expression ")" | "not" expression | "-" expression | function | object | array
    complex_expression = simple_expression { "[" expression "]" | "." identifier | arguments }  
    arithmetic_factor = complex_expression
    arithmetic_term = arithmetic_factor { ("*" | "/") arithmetic_factor }
    arithmetic_expression = arithmetic_term { ("+" | "-") arithmetic_term }
    relational_expression = arithmetic_expression { ("<" | ">" | "<=" | ">=" | "==" | "!=") arithmetic_expression }
    logical_factor = relational_expression
    logical_term = logical_factor { "&&" logical_factor }
    logical_expression = logical_term { "||" logical_term }
    expression = logical_expression
    print_statement = "print" [ expression ]
    if_statement = "if" "(" expression ")" block [ "else" block ]
    while_statement = "while" "(" expression ")" block
    return_statement = "return" [ expression ]
    assignment_statement = expression [ "=" expression ]
    function_statement = "function" identifier parameters block
    statement = if_statement | while_statement | print_statement | function_statement | return_statement | assignment_statement
    program = [ statement { ";" statement } ]
"""

def parse_parameters(tokens):
    """
    parameters = "(" [ identifier { "," identifier } ] ")"
    """
    assert tokens[0]["tag"] == "(", f"Expected '(' but got {tokens[0]}"
    tokens = tokens[1:]
    identifiers = []
    if tokens[0]["tag"] != ")":
        if tokens[0]["tag"] == "identifier":
            identifiers.append({"tag": "identifier", "value": tokens[0]["value"]})
            tokens = tokens[1:]
        else:
            raise Exception(f"Expected identifier but got {tokens[0]}")
        while tokens[0]["tag"] == ",":
            tokens = tokens[1:]
            if tokens[0]["tag"] == "identifier":
                identifiers.append({"tag": "identifier", "value": tokens[0]["value"]})
                tokens = tokens[1:]
            else:
                raise Exception(f"Expected identifier but got {tokens[0]}")
    assert tokens[0]["tag"] == ")", f"Expected ')' but got {tokens[0]}"
    return {"tag": "parameters", "identifiers": identifiers}, tokens[1:]

def test_parse_parameters():
    """
    parameters = "(" [ identifier { "," identifier } ] ")"
    """
    print("testing parse_parameters...")
    # Test empty list
    tokens = tokenize("()")
    ast, tokens = parse_parameters(tokens)
    expected = {"tag": "parameters", "identifiers": []}
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

    # Test one identifier
    tokens = tokenize("(x)")
    ast, tokens = parse_parameters(tokens)
    expected = {"tag": "parameters", "identifiers": [{"tag": "identifier", "value": "x"}]}
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

    # Test multiple identifiers
    tokens = tokenize("(x,y,z)")
    ast, tokens = parse_parameters(tokens)
    expected = {
        "tag": "parameters",
        "identifiers": [
            {"tag": "identifier", "value": "x"},
            {"tag": "identifier", "value": "y"},
            {"tag": "identifier", "value": "z"},
        ],
    }
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

def parse_arguments(tokens):
    """
    arguments = "(" [ expression { "," expression } ] ")"
    """
    assert tokens[0]["tag"] == "(", f"Expected '(' but got {tokens[0]}"
    tokens = tokens[1:]
    values = []
    if tokens[0]["tag"] != ")":
        expr, tokens = parse_expression(tokens)
        values.append(expr)
        while tokens[0]["tag"] == ",":
            tokens = tokens[1:]
            expr, tokens = parse_expression(tokens)
            values.append(expr)
    assert tokens[0]["tag"] == ")", f"Expected ')' but got {tokens[0]}"
    return {"tag": "arguments", "values": values}, tokens[1:]

def test_parse_arguments():
    """
    arguments = "(" [ expression { "," expression } ] ")"
    """
    print("testing parse_arguments...")
    # Test empty list
    tokens = tokenize("()")
    ast, tokens = parse_arguments(tokens)
    expected = {"tag": "arguments", "values": []}
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

    # Test one expression
    tokens = tokenize("(1)")
    ast, tokens = parse_arguments(tokens)
    expected = {"tag": "arguments", "values": [{"tag": "number", "value": 1}]}
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

    # Test multiple expressions
    tokens = tokenize("(1,2,3)")
    ast, tokens = parse_arguments(tokens)
    expected = {
        "tag": "arguments",
        "values": [
            {"tag": "number", "value": 1},
            {"tag": "number", "value": 2},
            {"tag": "number", "value": 3},
        ],
    }
    assert ast == expected, f"Expected {expected}, got {ast}"
    assert tokens[0]["tag"] is None

def parse_block(tokens):
    """
    block = "{" statement { ";" statement } "}"
    """
    expected_tag = "{"
    assert tokens[0]["tag"] == expected_tag, f"Expected '{expected_tag}' but got {tokens[0]}"
    tokens = tokens[1:]
    statements = []
    if tokens[0]["tag"] != "}":
        statement, tokens = parse_statement(tokens)
        statements.append(statement)
        while tokens[0]["tag"] == ";":
            tokens = tokens[1:]
            statement, tokens = parse_statement(tokens)
            statements.append(statement)
    expected_tag = "}"
    assert tokens[0]["tag"] == expected_tag, f"Expected '{expected_tag}' but got {tokens[0]}"
    return {"tag": "block", "statements": statements}, tokens[1:]


def test_parse_block():
    """
    block = "{" statement { ";" statement } "}"
    """
    print("testing parse_block")
    tokens = tokenize("{1;2;3}")
    ast, tokens = parse_block(tokens)

def parse_array(tokens):
    """
    array = "[" [ expression { "," expression } ] "]"
    """
    assert tokens[0]["tag"] == "[", f"Expected '[' but got {tokens[0]}"
    tokens = tokens[1:]
    values = []
    if tokens[0]["tag"] != "]":
        expr, tokens = parse_expression(tokens)
        values.append(expr)
        while tokens[0]["tag"] == ",":
            tokens = tokens[1:]
            expr, tokens = parse_expression(tokens)
            values.append(expr)
    assert tokens[0]["tag"] == "]", f"Expected ']' but got {tokens[0]}"
    return {"tag": "array", "values": values}, tokens[1:]

def test_parse_array():
    """
    array = "[" [ expression { "," expression } ] "]"
    """
    print("testing parse_array...")
    # Test empty array literal
    tokens = tokenize("[]")
    ast, tokens = parse_array(tokens)
    assert ast == {'tag': 'array', 'values': []}
    assert tokens[0]["tag"] is None
    # Test single array literal
    tokens = tokenize("[1]")
    ast, tokens = parse_array(tokens)
    assert ast == {'tag': 'array', 'values': [{'tag': 'number', 'value': 1}]}
    assert tokens[0]["tag"] is None
    tokens = tokenize("[1,2,3]")
    ast, tokens = parse_array(tokens)
    assert ast == {'tag': 'array', 'values': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}]}
    tokens = tokenize("[1,2,3,[4,5]]")
    ast, tokens = parse_array(tokens)
    assert ast == {'tag': 'array', 'values': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}, {'tag': 'array', 'values': [{'tag': 'number', 'value': 4}, {'tag': 'number', 'value': 5}]}]}
    assert tokens[0]["tag"] is None

def parse_object(tokens):
    """
    object = "{" [ (string | identifier) ":" expression { "," (string | identifier) ":" expression } ] "}"
    """
    expected_tag = "{"
    assert tokens[0]["tag"] == expected_tag, f"Expected '{expected_tag}' but got {tokens[0]}"
    tokens = tokens[1:]
    values = []
    if tokens[0]["tag"] != "}":
        assert tokens[0]["tag"] in ["string","identifier"]
        key = tokens[0]["value"]
        tokens = tokens[1:]
        assert tokens[0]["tag"] == ":"
        tokens = tokens[1:]
        expr, tokens = parse_expression(tokens)
        values.append({"key":key, "value":expr})
        while tokens[0]["tag"] == ",":
            tokens = tokens[1:]
            assert tokens[0]["tag"] in ["string","identifier"]
            key = tokens[0]["value"]
            tokens = tokens[1:]
            assert tokens[0]["tag"] == ":"
            tokens = tokens[1:]
            expr, tokens = parse_expression(tokens)
            values.append({"key":key, "value":expr})
    expected_tag = "}"
    assert tokens[0]["tag"] == expected_tag, f"Expected '{expected_tag}' but got {tokens[0]}"
    return {"tag": "object", "values": values}, tokens[1:]

def test_parse_object():
    """
    object = "{" [ (string | identifier) ":" expression { "," (string | identifier) ":" expression } ] "}"
    """
    print("testing parse_object...")
    # Test empty object literal
    tokens = tokenize("{}")
    ast, tokens = parse_object(tokens)
    assert ast == {'tag': 'object', 'values': []}
    assert tokens[0]["tag"] is None
    # Test single key object literal
    tokens = tokenize("{x:1}")
    ast, tokens = parse_object(tokens)
    assert ast == {'tag': 'object', 'values': [{'key': 'x', 'value': {'tag': 'number', 'value': 1}}]}
    assert tokens[0]["tag"] is None
    # Test multiple key object literal
    tokens = tokenize("{x:1, y:2, z:3}")
    ast, tokens = parse_object(tokens)
    assert ast == {'tag': 'object', 'values': [{'key': 'x', 'value': {'tag': 'number', 'value': 1}}, {'key': 'y', 'value': {'tag': 'number', 'value': 2}}, {'key': 'z', 'value': {'tag': 'number', 'value': 3}}]}
    assert tokens[0]["tag"] is None
    # Test nested object literal
    tokens = tokenize("{x:1, y:2, z:{a:1,b:2,c:[1,2,3]}}")
    ast, tokens = parse_object(tokens)
    assert ast == {'tag': 'object', 'values': [{'key': 'x', 'value': {'tag': 'number', 'value': 1}}, {'key': 'y', 'value': {'tag': 'number', 'value': 2}}, {'key': 'z', 'value': {'tag': 'object', 'values': [{'key': 'a', 'value': {'tag': 'number', 'value': 1}}, {'key': 'b', 'value': {'tag': 'number', 'value': 2}}, {'key': 'c', 'value': {'tag': 'array', 'values': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}]}}]}}]}    

def parse_function(tokens):
    """
    function = "function" parameters block
    """
    assert tokens[0]["tag"] == "function", f"Expected '{function}' but got {tokens[0]}"
    tokens = tokens[1:]
    parameters, tokens = parse_parameters(tokens)
    block, tokens = parse_block(tokens)
    ast = {
        "tag":"function",
        "parameters" : parameters["identifiers"],
        "body" : block["statements"]
    }    
    return ast, tokens

def test_parse_function():
    """
    function = "function" parameters block
    """
    print("testing parse_function...")
    ast, tokens = parse_function(tokenize("function (x) {}"))
    assert ast == {'tag': 'function', 'parameters': [{'tag': 'identifier', 'value': 'x'}], 'body': []}    
    assert tokens[0]["tag"] == None

# EXPRESSIONS

def parse_simple_expression(tokens):
    """
    simple_expression = <number> | <string> | <identifier> | "(" expression ")" | "not" expression | "-" expression | function | object | array
    """
    token = tokens[0]
    if token["tag"] == "number":
        return {"tag": "number", "value": token["value"]}, tokens[1:]
    if token["tag"] == "string":
        return {"tag": "string", "value": token["value"]}, tokens[1:]
    if token["tag"] == "identifier":
        return {"tag": "identifier", "value": token["value"]}, tokens[1:]
    if token["tag"] == "(":
        ast, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", f"Expected ')' but got {tokens[0]}"
        return ast, tokens[1:]
    if token["tag"] == "not":
        ast, tokens = parse_expression(tokens[1:])
        return {"tag": "not", "value": ast}, tokens
    if token["tag"] == "-":
        ast, tokens = parse_expression(tokens[1:])
        return {"tag": "negate", "value": ast}, tokens
    if token["tag"] == "function":
        ast, tokens = parse_function(tokens)
        return ast, tokens
    if token["tag"] == "[":
        return parse_array(tokens)
    if token["tag"] == "{":
        return parse_object(tokens)    
    raise Exception(f"Unexpected token '{token['tag']}' at position {token['position']}.")

def test_parse_simple_expression():
    """
    simple_expression = <number> | <string> | <identifier> | "(" expression ")" | "not" expression | "-" expression | function | object | array
    """
    print("testing parse_simple_expression()")
    for s in ["1", "22", "333"]:
        tokens = tokenize(s)
        ast, tokens = parse_simple_expression(tokens)
        assert ast == {"tag": "number", "value": int(s)}
        assert tokens[0]["tag"] is None
    for s in ["\"a\"", "\"bb\"", "\"ccc\""]:
        tokens = tokenize(s)
        ast, tokens = parse_simple_expression(tokens)
        assert ast == {"tag": "string", "value": s[1:-1]}
        assert tokens[0]["tag"] is None
    for s in ["a", "bb", "ccc"]:
        tokens = tokenize(s)
        ast, tokens = parse_simple_expression(tokens)
        assert ast == {"tag": "identifier", "value": s}
        assert tokens[0]["tag"] is None
    for s in ["(1)", "(22)"]:
        tokens = tokenize(s)
        ast, tokens = parse_simple_expression(tokens)
        s_n = s.replace("(", "").replace(")", "")
        assert ast == {"tag": "number", "value": int(s_n)}
        assert tokens[0]["tag"] is None
    tokens = tokenize("! 1")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {'tag': 'not', 'value': {'tag': 'number', 'value': 1}}
    tokens = tokenize("not 1")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {'tag': 'not', 'value': {'tag': 'number', 'value': 1}}
    tokens = tokenize("function(x) {}")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {'tag': 'function', 'parameters': [{'tag': 'identifier', 'value': 'x'}], 'body': []}
    assert tokens[0]["tag"] == None

def parse_complex_expression(tokens):
    """
    complex_expression = simple_expression { "[" expression "]" | "." identifier | arguments }  
    """
    ast, tokens = parse_simple_expression(tokens)
    while True:
        if tokens[0]["tag"] == "[":
            tokens = tokens[1:]
            index, tokens = parse_expression(tokens)
            ast = {
                "tag":"index",
                "object":ast,
                "index":index
            }
            assert tokens[0]["tag"] == "]", f"Expected ']' but got {tokens[0]}"
            tokens = tokens[1:]
        elif tokens[0]["tag"] == ".":
            tokens = tokens[1:]
            assert tokens[0]["tag"] == "identifier", "Expected property name"
            property = tokens[0]["value"]
            ast = {
                "tag": "member",
                "object": ast,
                "property": property
            }
            tokens = tokens[1:]
        elif tokens[0]["tag"] == "(":
            arguments, tokens = parse_arguments(tokens)
            ast = {
                "tag":"call",
                "function":ast,
                "arguments":arguments
            }
        else:
            break
    return ast, tokens

def test_parse_complex_expression():
    """
    complex_expression = simple_expression { "[" expression "]" | "." identifier | arguments }  
    """
    print("testing parse_complex_expression()")
    tokens = tokenize("123")
    ast, tokens = parse_complex_expression(tokens)
    assert ast == {'tag': 'number', 'value': 123}
    tokens = tokenize("x[1]")
    ast, tokens = parse_complex_expression(tokens)
    assert ast == {'tag': 'index', 'object': {'tag': 'identifier', 'value': 'x'}, 'index': {'tag': 'number', 'value': 1}}
    assert tokens[0]["tag"] is None
    tokens = tokenize("x.foo")
    ast, tokens = parse_complex_expression(tokens)
    assert ast == {'tag': 'member', 'object': {'tag': 'identifier', 'value': 'x'}, 'property': 'foo'}
    assert tokens[0]["tag"] is None
    tokens = tokenize("x(1,2,3)")
    ast, tokens = parse_complex_expression(tokens)
    assert ast == {'tag': 'call', 'function': {'tag': 'identifier', 'value': 'x'}, 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}]}}
    assert tokens[0]["tag"] is None
    tokens = tokenize("x(1,2,3)[2].foo(4)")
    ast, tokens = parse_complex_expression(tokens)
    assert ast == {'tag': 'call', 'function': {'tag': 'member', 'object': {'tag': 'index', 'object': {'tag': 'call', 'function': {'tag': 'identifier', 'value': 'x'}, 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}]}}, 'index': {'tag': 'number', 'value': 2}}, 'property': 'foo'}, 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 4}]}}
    assert tokens[0]["tag"] is None
    tokens = tokenize("x.y().z.a")
    ast, tokens = parse_complex_expression(tokens)
    assert ast == {'tag': 'member', 'object': {'tag': 'member', 'object': {'tag': 'call', 'function': {'tag': 'member', 'object': {'tag': 'identifier', 'value': 'x'}, 'property': 'y'}, 'arguments': {'tag': 'arguments', 'values': []}}, 'property': 'z'}, 'property': 'a'}
    tokens = tokenize("(f().x)(3)[4]")
    ast, tokens = parse_complex_expression(tokens)
    assert ast == {'tag': 'index', 'object': {'tag': 'call', 'function': {'tag': 'member', 'object': {'tag': 'call', 'function': {'tag': 'identifier', 'value': 'f'}, 'arguments': {'tag': 'arguments', 'values': []}}, 'property': 'x'}, 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 3}]}}, 'index': {'tag': 'number', 'value': 4}}
    tokens = tokenize("obj.method(arg1, arg2)[key].subprop")
    ast, tokens = parse_complex_expression(tokens)
    assert ast == {'tag': 'member', 'object': {'tag': 'index', 'object': {'tag': 'call', 'function': {'tag': 'member', 'object': {'tag': 'identifier', 'value': 'obj'}, 'property': 'method'}, 'arguments': {'tag': 'arguments', 'values': [{'tag': 'identifier', 'value': 'arg1'}, {'tag': 'identifier', 'value': 'arg2'}]}}, 'index': {'tag': 'identifier', 'value': 'key'}}, 'property': 'subprop'}    

def parse_arithmetic_factor(tokens):
    """
    arithmetic_factor = complex_expression
    """
    return parse_complex_expression(tokens)


def test_parse_arithmetic_factor():
    """
    arithmetic_factor = complex_expression
    """
    print("testing parse_arithmetic_factor()")
    tokens = tokenize("obj.method(arg1, arg2)[key].subprop")
    ast, tokens = parse_complex_expression(tokens)
    assert ast == {'tag': 'member', 'object': {'tag': 'index', 'object': {'tag': 'call', 'function': {'tag': 'member', 'object': {'tag': 'identifier', 'value': 'obj'}, 'property': 'method'}, 'arguments': {'tag': 'arguments', 'values': [{'tag': 'identifier', 'value': 'arg1'}, {'tag': 'identifier', 'value': 'arg2'}]}}, 'index': {'tag': 'identifier', 'value': 'key'}}, 'property': 'subprop'}   

def parse_arithmetic_term(tokens):
    """
    arithmetic_term = arithmetic_factor { ("*" | "/") arithmetic_factor }
    """
    node, tokens = parse_arithmetic_factor(tokens)
    while tokens[0]["tag"] in ["*", "/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_arithmetic_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_arithmetic_term():
    """
    arithmetic_term = arithmetic_factor { ("*" | "/") arithmetic_factor }
    """
    print("testing parse_arithmetic_term()")

    for s in ["1", "22", "333"]:
        tokens = tokenize(s)
        ast, tokens = parse_arithmetic_term(tokens)
        assert ast == {"tag": "number", "value": int(s)}
        assert tokens[0]["tag"] is None
    tokens = tokenize("2*4")
    ast, tokens = parse_arithmetic_term(tokens)
    assert ast == {
        "tag": "*",
        "left": {"tag": "number", "value": 2},
        "right": {"tag": "number", "value": 4},
    }
    tokens = tokenize("2*4/6")
    ast, tokens = parse_arithmetic_term(tokens)
    assert ast == {
        "tag": "/",
        "left": {
            "tag": "*",
            "left": {"tag": "number", "value": 2},
            "right": {"tag": "number", "value": 4},
        },
        "right": {"tag": "number", "value": 6},
    }

def parse_arithmetic_expression(tokens):
    """
    arithmetic_expression = arithmetic_term { ("+" | "-") arithmetic_term }
    """
    ast, tokens = parse_arithmetic_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_arithmetic_term(tokens[1:])
        ast = {"tag": tag, "left": ast, "right": right_node}
    return ast, tokens

def test_parse_arithmetic_expression():
    """
    arithmetic_expression = arithmetic_term { ("+" | "-") arithmetic_term }
    """
    print("testing parse_arithmetic_expression()")
    for s in ["1", "22", "333"]:
        tokens = tokenize(s)
        ast, tokens = parse_arithmetic_expression(tokens)
        assert ast == {"tag": "number", "value": int(s)}
        assert tokens[0]["tag"] is None
    tokens = tokenize("2*4")
    ast, tokens = parse_arithmetic_expression(tokens)
    assert ast == {
        "tag": "*",
        "left": {"tag": "number", "value": 2},
        "right": {"tag": "number", "value": 4},
    }
    tokens = tokenize("1+2*4")
    ast, tokens = parse_arithmetic_expression(tokens)
    assert ast == {
        "tag": "+",
        "left": {"tag": "number", "value": 1},
        "right": {
            "tag": "*",
            "left": {"tag": "number", "value": 2},
            "right": {"tag": "number", "value": 4},
        },
    }
    tokens = tokenize("1+(2+3)*4")
    ast, tokens = parse_arithmetic_expression(tokens)
    assert ast == {
        "tag": "+",
        "left": {"tag": "number", "value": 1},
        "right": {
            "tag": "*",
            "left": {
                "tag": "+",
                "left": {"tag": "number", "value": 2},
                "right": {"tag": "number", "value": 3},
            },
            "right": {"tag": "number", "value": 4},
        },
    }

def parse_relational_expression(tokens):
    """
    relational_expression = arithmetic_expression { ("<" | ">" | "<=" | ">=" | "==" | "!=") arithmetic_expression }
    """
    node, tokens = parse_arithmetic_expression(tokens)
    while tokens[0]["tag"] in ["<", ">", "<=", ">=", "==", "!="]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_arithmetic_expression(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens

def test_parse_relational_expression():
    """
    relational_expression = arithmetic_expression { ("<" | ">" | "<=" | ">=" | "==" | "!=") arithmetic_expression }
    """
    print("testing parse_relational_expression()")
    for operator in ["<", ">", "<=", ">=", "==", "!="]:
        tokens = tokenize(f"2{operator}4")
        ast, tokens = parse_relational_expression(tokens)
        assert ast == {
            "tag": operator,
            "left": {"tag": "number", "value": 2},
            "right": {"tag": "number", "value": 4},
        }, f"AST = [{ast}]"
    tokens = tokenize("2>4==3")
    ast, tokens = parse_relational_expression(tokens)
    assert ast == {
        "tag": "==",
        "left": {"tag": ">", "left": {"tag": "number", "value": 2}, "right": {"tag": "number", "value": 4}},
        "right": {"tag": "number", "value": 3},
    }
    tokens = tokenize("x<y>z")
    ast, tokens = parse_relational_expression(tokens)
    assert ast == {
        "tag": ">",
        "left": {
            "tag": "<",
            "left": {"tag": "identifier", "value": "x"},
            "right": {"tag": "identifier", "value": "y"},
        },
        "right": {"tag": "identifier", "value": "z"},
    }

def parse_logical_factor(tokens):
    """
    logical_factor = relational_expression
    """
    return parse_relational_expression(tokens)

def test_parse_logical_factor():
    """
    logical_factor = relational_expression
    """
    print("testing parse_logical_factor...")
    tokens = tokenize("x")
    ast, tokens = parse_logical_factor(tokens)
    assert ast == {"tag": "identifier", "value": "x"}
    tokens = tokenize("!x")
    ast, tokens = parse_logical_factor(tokens)
    assert ast == {
        "tag": "not",
        "value": {"tag": "identifier", "value": "x"},
    }
    tokens = tokenize("not x")
    ast, tokens = parse_logical_factor(tokens)
    assert ast == {
        "tag": "not",
        "value": {"tag": "identifier", "value": "x"},
    }

def parse_logical_term(tokens):
    """
    logical_term = logical_factor { "&&" logical_factor }
    """
    node, tokens = parse_logical_factor(tokens)
    while tokens[0]["tag"] == "and":
        tag = tokens[0]["tag"]
        next_node, tokens = parse_logical_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": next_node}
    return node, tokens

def test_parse_logical_term():
    """
    logical_term = logical_factor { "&&" logical_factor }
    """
    print("testing parse_logical_term...")
    tokens = tokenize("x")
    ast, tokens = parse_logical_term(tokens)
    assert ast == {"tag": "identifier", "value": "x"}
    tokens = tokenize("x&&y")
    ast, tokens = parse_logical_term(tokens)
    assert ast == {
        "tag": "and",
        "left": {"tag": "identifier", "value": "x"},
        "right": {"tag": "identifier", "value": "y"},
    }
    tokens = tokenize("x&&y&&z")
    ast, tokens = parse_logical_term(tokens)
    assert ast == {
        "tag": "and",
        "left": {
            "tag": "and",
            "left": {"tag": "identifier", "value": "x"},
            "right": {"tag": "identifier", "value": "y"},
        },
        "right": {"tag": "identifier", "value": "z"},
    }

def parse_logical_expression(tokens):
    """
    logical_expression = logical_term { "||" logical_term }
    """
    node, tokens = parse_logical_term(tokens)
    while tokens[0]["tag"] == "or":
        tag = tokens[0]["tag"]
        next_node, tokens = parse_logical_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": next_node}
    return node, tokens

def test_parse_logical_expression():
    """
    logical_expression = logical_term { "||" logical_term }
    """
    print("testing parse_logical_expression...")
    tokens = tokenize("x")
    ast, tokens = parse_logical_expression(tokens)
    assert ast == {"tag": "identifier", "value": "x"}
    tokens = tokenize("x||y")
    ast, tokens = parse_logical_expression(tokens)
    assert ast == {
        "tag": "or",
        "left": {"tag": "identifier", "value": "x"},
        "right": {"tag": "identifier", "value": "y"},
    }
    tokens = tokenize("x||y&&z")
    ast, tokens = parse_logical_expression(tokens)
    assert ast == {
        "tag": "or",
        "left": {"tag": "identifier", "value": "x"},
        "right": {
            "tag": "and",
            "left": {"tag": "identifier", "value": "y"},
            "right": {"tag": "identifier", "value": "z"},
        },
    }
    tokens = tokenize("x or y and z")
    ast, tokens = parse_logical_expression(tokens)
    assert ast == {
        "tag": "or",
        "left": {"tag": "identifier", "value": "x"},
        "right": {
            "tag": "and",
            "left": {"tag": "identifier", "value": "y"},
            "right": {"tag": "identifier", "value": "z"},
        },
    }


def parse_expression(tokens):
    """
    expression = logical_expression
    """
    return parse_logical_expression(tokens)
    

def test_parse_expression():
    """
    expression = logical_expression
    """
    print("testing parse_expression...")
    return True

# STATEMENTS

def parse_print_statement(tokens):
    """
    print_statement = "print" [ expression ]
    """
    assert tokens[0]["tag"] == "print", f"Expected 'print', got {tokens[0]}"
    tokens = tokens[1:]
    assert tokens[0]["tag"] == "(", f"Expected \"(\", got {tokens[0]}"
    arguments, tokens = parse_arguments(tokens)
    return {"tag": "print", "arguments": arguments}, tokens

def test_parse_print_statement():
    """
    print_statement = "print" [ expression ]
    """
    print("testing parse_print_statement...")
    ast, tokens = parse_print_statement(tokenize("print(1)"))
    assert ast == {'tag': 'print', 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 1}]}}
    assert tokens[0]["tag"] is None
    ast, tokens = parse_print_statement(tokenize("print(1,2,3)"))
    assert ast == {'tag': 'print', 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}]}}
    assert tokens[0]["tag"] is None

def parse_if_statement(tokens):
    """
    if_statement = "if" "(" expression ")" block [ "else" block ]
    """
    assert tokens[0]["tag"] == "if", f"Expected 'if', got {tokens[0]}"
    tokens = tokens[1:]
    assert tokens[0]["tag"] == "(", f"Expected '(', got {tokens[0]}"
    tokens = tokens[1:]
    condition, tokens = parse_expression(tokens)
    assert tokens[0]["tag"] == ")", f"Expected ')', got {tokens[0]}"
    tokens = tokens[1:]
    then_statement, tokens = parse_block(tokens)
    else_statement = None
    if tokens[0]["tag"] == "else":
        tokens = tokens[1:]
        else_statement, tokens = parse_block(tokens)
    ast = {
        "tag": "if",
        "condition": condition,
        "then": then_statement,
        "else": else_statement,
    }
    return ast, tokens

def test_parse_if_statement():
    """
    if_statement = "if" "(" expression ")" block [ "else" block ]
    """
    ast, _ = parse_if_statement(tokenize("if(1){print(1)}"))
    assert ast == {'tag': 'if', 'condition': {'tag': 'number', 'value': 1}, 'then': {'tag': 'block', 'statements': [{'tag': 'print', 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 1}]}}]}, 'else': None}
    ast, _ = parse_if_statement(tokenize("if(1){print(1)}else{print(2)}"))
    assert ast == {'tag': 'if', 'condition': {'tag': 'number', 'value': 1}, 'then': {'tag': 'block', 'statements': [{'tag': 'print', 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 1}]}}]}, 'else': {'tag': 'block', 'statements': [{'tag': 'print', 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 2}]}}]}}

def parse_while_statement(tokens):
    """
    while_statement = "while" "(" expression ")" block
    """
    assert tokens[0]["tag"] == "while", f"Expected 'while', got {tokens[0]}"
    tokens = tokens[1:]
    assert tokens[0]["tag"] == "(", f"Expected '(', got {tokens[0]}"
    tokens = tokens[1:]
    condition, tokens = parse_expression(tokens)
    assert tokens[0]["tag"] == ")", f"Expected ')', got {tokens[0]}"
    tokens = tokens[1:]
    do_statement, tokens = parse_block(tokens)
    ast = {
        "tag": "while",
        "condition": condition,
        "do": do_statement,
    }
    return ast, tokens

def test_parse_while_statement():
    """
    while_statement = "while" "(" expression ")" block
    """
    ast, _ = parse_while_statement(tokenize("while(1){print(1)}"))
    assert ast == {'tag': 'while', 'condition': {'tag': 'number', 'value': 1}, 'do': {'tag': 'block', 'statements': [{'tag': 'print', 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 1}]}}]}}

def parse_return_statement(tokens):
    """
    return_statement = "return" [ expression ]
    """
    assert tokens[0]["tag"] == "return", f"Expected 'return', got {tokens[0]}"
    tokens = tokens[1:]
    if tokens[0]["tag"] not in [None, ";", "}"]:
        expr, tokens = parse_expression(tokens)
        return {"tag": "return", "value": expr}, tokens
    return {"tag": "return", "value": None}, tokens

def test_parse_return_statement():
    """
    return_statement = "return" [ expression ]
    """
    print("testing parse_return_statement...")
    
    # Return with no expression
    tokens = tokenize("return")
    ast, tokens = parse_return_statement(tokens)
    assert ast == {"tag": "return", "value": None}
    assert tokens[0]["tag"] is None

    # Return with a number
    tokens = tokenize("return 42")
    ast, tokens = parse_return_statement(tokens)
    assert ast == {"tag": "return", "value": {"tag": "number", "value": 42}}
    assert tokens[0]["tag"] is None

    # Return with an expression
    tokens = tokenize("return 1 + 2 * 3")
    ast, tokens = parse_return_statement(tokens)
    assert ast == {
        "tag": "return",
        "value": {
            "tag": "+",
            "left": {"tag": "number", "value": 1},
            "right": {
                "tag": "*",
                "left": {"tag": "number", "value": 2},
                "right": {"tag": "number", "value": 3}
            }
        }
    }
    assert tokens[0]["tag"] is None

def parse_assignment_statement(tokens):
    """
    assignment_statement = expression [ "=" expression ]
    """
    target, tokens = parse_expression(tokens)
    if tokens[0]["tag"] == "=":
        tokens = tokens[1:]
        value, tokens = parse_expression(tokens)
        return {"tag": "assign", "target": target, "value": value}, tokens
    return target, tokens

def test_parse_assignment_statement():
    """
    assignment_statement = expression [ "=" expression ]
    """
    print("testing parse_assignment_statement()")
    ast, tokens = parse_assignment_statement(tokenize("i=2"))
    assert ast == {
        "tag": "assign",
        "target": {"tag": "identifier", "value": "i"},
        "value": {"tag": "number", "value": 2},
    }
    ast, tokens = parse_assignment_statement(tokenize("2"))
    assert ast == {"tag": "number", "value": 2}

def parse_function_statement(tokens):
    """
    function_statement = "function" identifier parameters block
    """
    function_token = tokens[0]
    identifier_token = tokens[1]
    assignment_token = {'tag': '=', 'position': identifier_token["position"], 'value': '='}
    tokens = [identifier_token, assignment_token, function_token ] + tokens[2:]
    return parse_assignment_statement(tokens)

def test_parse_function_statement():
    """
    function_statement = "function" identifier parameters block
    """
    tokens = tokenize("foo = function (x) {}")
    ast1, _ = parse_assignment_statement(tokens)
    tokens = tokenize("function foo(x) {}")
    ast2, _ = parse_function_statement(tokens)
    assert ast1 == ast2
    assert ast2 == {'tag': 'assign', 'target': {'tag': 'identifier', 'value': 'foo'}, 'value': {'tag': 'function', 'parameters': [{'tag': 'identifier', 'value': 'x'}], 'body': []}}

def parse_statement(tokens):
    """
    statement = if_statement | while_statement | print_statement | function_statement | return_statement | assignment_statement
    """
    tag = tokens[0]["tag"]
    if tag == "{":
        return parse_block(tokens)
    if tag == "if":
        return parse_if_statement(tokens)
    if tag == "while":
        return parse_while_statement(tokens)
    if tag == "print":
        return parse_print_statement(tokens)
    if tag == "function":
        return parse_function_statement(tokens)
    return parse_assignment_statement(tokens)

def test_parse_statement():
    """
    statement = if_statement | while_statement | print_statement | function_statement | return_statement | assignment_statement
    """
    print("testing parse_statement...")
    ast, _ = parse_statement(tokenize("print(1)"))
    assert ast =={'tag': 'print', 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 1}]}}
    ast, _ = parse_statement(tokenize("x=3"))
    assert ast == {"tag": "assign", "target": {"tag": "identifier", "value": "x"}, "value": {"tag": "number", "value": 3}}

def parse_program(tokens):
    """
    program = [ statement { ";" statement } ]
    """
    statements = []
    if tokens[0]["tag"]:
        statement, tokens = parse_statement(tokens)
        statements.append(statement)
        while tokens[0]["tag"] == ";":
            tokens = tokens[1:]
            statement, tokens = parse_statement(tokens)
            statements.append(statement)
    assert tokens[0]["tag"] is None, f"Expected end of input at position {tokens[0]['position']}, got [{tokens[0]}]"
    return {"tag": "program", "statements": statements}, tokens[1:]

def test_parse_program():
    """
    program = [ statement { ";" statement } ]
    """
    print("testing parse_program...")
    ast, tokens = parse_program(tokenize("print(1); print(2)"))
    assert ast == {'tag': 'program', 'statements': [{'tag': 'print', 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 1}]}}, {'tag': 'print', 'arguments': {'tag': 'arguments', 'values': [{'tag': 'number', 'value': 2}]}}]}

def parse(tokens):
    ast, tokens = parse_program(tokens)
    return ast


# --- Grammar Verification Mechanism ---

# Normalize the grammar by stripping whitespace from each nonempty line.
grammar = grammar.split("\n")
grammar = [line.strip() for line in grammar if line.strip() != ""]
for line in grammar:
    print(line)

if __name__ == "__main__":
    # List of all test functions.
    test_functions = [
        test_parse_parameters,
        test_parse_arguments,
        test_parse_block,
        test_parse_array,
        test_parse_object,
        test_parse_function,
        test_parse_simple_expression,
        test_parse_complex_expression,
        test_parse_arithmetic_factor,
        test_parse_arithmetic_term,
        test_parse_arithmetic_expression,
        test_parse_relational_expression,
        test_parse_logical_factor,
        test_parse_logical_term,
        test_parse_logical_expression,
        test_parse_expression,
        test_parse_print_statement,
        test_parse_if_statement,
        test_parse_while_statement,
        test_parse_return_statement,
        test_parse_assignment_statement,
        test_parse_function_statement,
        test_parse_statement,
        test_parse_program
    ]

    untested_grammar = grammar

    # For each test function, verify that:
    # 1. Its docstring rule appears in the normalized grammar.
    # 2. The corresponding parsing function shares the same docstring rule.
    for test_func in test_functions:
        test_rule = test_func.__doc__.strip().splitlines()[0].strip()
        # print("Testing rule from test:", test_rule)
        if test_rule not in untested_grammar:
            raise Exception(f"Rule [{test_rule}] not found in grammar.")
        untested_grammar = [line for line in untested_grammar if line != test_rule]

        # Determine the corresponding parsing function name (drop the "test_" prefix).
        parsing_func_name = test_func.__name__[5:]
        if parsing_func_name not in globals():
            raise Exception(f"Parsing function {parsing_func_name} not found for test {test_func.__name__}")
        parsing_func = globals()[parsing_func_name]
        if not parsing_func.__doc__:
            raise Exception(f"Parsing function {parsing_func_name} has no docstring.")
        func_rule = parsing_func.__doc__.strip().splitlines()[0].strip()
        if test_rule != func_rule:
            raise Exception(
                f"Mismatch in docstring rules for {parsing_func_name}: "
                f"test rule is [{test_rule}] but function rule is [{func_rule}]."
            )
        # Run the test function.
        test_func()

    if len(untested_grammar) > 0:
        print("Untested grammar rules:")
        print(untested_grammar)
    else:
        print("All grammar rules are covered.")

    print("done.")