from tokenizer import tokenize

"""
parser.py -- implement parser for simple expressions

Accept a string of tokens, return an AST expressed as stack of dictionaries
"""

"""
    factor = <number> | <identifier> | "(" expression ")" | "!" expression | "-" expression
    term = factor { "*"|"/" factor }
    arithmetic_expression = term { "+"|"-" term }
    relational_expression = arithmetic_expression { ("<" | ">" | "<=" | ">=" | "==" | "!=") arithmetic_expression } ;
    # logical_factor = relational_expression ;
    # logical_term = logical_factor { "&&" logical_factor } ;
    # logical_expression = logical_term { "||" logical_term } ;
    # expression = logical_expression; 
    assignment_statement = expression [ "=" expression ]
    statement = <print> expression | assignment_statement
    program = [ statement { ";" statement } ]
"""


def parse_factor(tokens):
    """
    factor = <number> | <identifier> | "(" expression ")" | "!" expression | "-" expression
    """
    token = tokens[0]
    if token["tag"] == "number":
        return {"tag": "number", "value": token["value"]}, tokens[1:]
    if token["tag"] == "identifier":
        return {"tag": "identifier", "value": token["value"]}, tokens[1:]
    if token["tag"] == "(":
        ast, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")"
        return ast, tokens[1:]
    if token["tag"] == "!":
        ast, tokens = parse_expression(tokens[1:])
        return {"tag": "!", "value": ast}, tokens
    if token["tag"] == "-":
        ast, tokens = parse_expression(tokens[1:])
        return {"tag": "negate", "value": ast}, tokens
    raise Exception(
        f"Unexpected token '{token['tag']}' at position {token['position']}."
    )


def test_parse_factor():
    """
    factor = <number> | <identifier> | "(" expression ")" | "!" expression | "-" expression
    """
    print("testing parse_factor()")
    for s in ["1", "22", "333"]:
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        assert ast == {"tag": "number", "value": int(s)}
        assert tokens[0]["tag"] == None
    for s in ["(1)", "(22)"]:
        tokens = tokenize(s)
        ast, tokens = parse_factor(tokens)
        s_n = s.replace("(", "").replace(")", "")
        assert ast == {"tag": "number", "value": int(s_n)}
        assert tokens[0]["tag"] == None
    tokens = tokenize("(2+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {
        "tag": "+",
        "left": {"tag": "number", "value": 2},
        "right": {"tag": "number", "value": 3},
    }
    tokens = tokenize("x")
    ast, tokens = parse_factor(tokens)
    assert ast == {"tag": "identifier", "value": "x"}
    tokens = tokenize("(x+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {
        "tag": "+",
        "left": {"tag": "identifier", "value": "x"},
        "right": {"tag": "number", "value": 3}
    }
    tokens = tokenize("-(x+3)")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': 'negate', 'value': {'tag': '+', 'left': {'tag': 'identifier', 'value': 'x'}, 'right': {'tag': 'number', 'value': 3}}}
    tokens = tokenize("!1")
    ast, tokens = parse_factor(tokens)
    assert ast == {'tag': '!', 'value': {'tag': 'number', 'value': 1}}


def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in ["*", "/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}

    return node, tokens


def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term()")
    for s in ["1", "22", "333"]:
        tokens = tokenize(s)
        ast, tokens = parse_term(tokens)
        assert ast == {"tag": "number", "value": int(s)}
        assert tokens[0]["tag"] == None
    tokens = tokenize("2*4")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "tag": "*",
        "left": {"tag": "number", "value": 2},
        "right": {"tag": "number", "value": 4},
    }
    tokens = tokenize("2*4/6")
    ast, tokens = parse_term(tokens)
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
    arithmetic_expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}

    return node, tokens


def test_parse_arithmetic_expression():
    """
    arithmetic_expression = term { "+"|"-" term }
    """
    print("testing parse_arithmetic_expression()")
    for s in ["1", "22", "333"]:
        tokens = tokenize(s)
        ast, tokens = parse_arithmetic_expression(tokens)
        assert ast == {"tag": "number", "value": int(s)}
        assert tokens[0]["tag"] == None
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
    # relational_expression = arithmetic_expression { ("<" | ">" | "<=" | ">=" | "==" | "!=") arithmetic_expression } ;
    """
    node, tokens = parse_arithmetic_expression(tokens)
    while tokens[0]["tag"] in ["<" , ">" , "<=" , ">=" , "==" , "!="]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_arithmetic_expression(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}

    return node, tokens

def test_parse_relational_expression():
    print("testing parse_relational_expression()")
    for operator in ["<" , ">" , "<=" , ">=" , "==" , "!="]:
        tokens = tokenize(f"2{operator}4")
        ast, tokens = parse_relational_expression(tokens)
        assert ast == {
            "tag": operator,
            "left": {"tag": "number", "value": 2},
            "right": {"tag": "number", "value": 4},
        }, f"AST = [{ast}]"
    tokens = tokenize("2>4==3")
    ast, tokens = parse_relational_expression(tokens)  
    assert ast=={'tag': '==', 'left': {'tag': '>', 'left': {'tag': 'number', 'value': 2}, 'right': {'tag': 'number', 'value': 4}}, 'right': {'tag': 'number', 'value': 3}}
    assert parse_relational_expression(tokenize("x<y>z"))[0] == {
        "tag": ">",
        "left": {
            "tag": "<",
            "left": {"tag": "identifier", "value": "x"},
            "right": {"tag": "identifier", "value": "y"},
        },
        "right": {"tag": "identifier", "value": "z"},
    }


# LOGICAL EXPRESSIONS


def parse_logical_factor(tokens):
    """
    logical_factor = relational_expression ;
    """
    return parse_relational_expression(tokens)


def test_parse_logical_factor():
    """
    logical_factor = relational_expression ;
    """
    print("testing parse_logical_factor...")
    assert parse_logical_factor(tokenize("x"))[0] == {"tag": "identifier", "value": "x"}
    assert parse_logical_factor(tokenize("!x"))[0] == {
        "tag": "!",
        "value": {"tag": "identifier", "value": "x"},
    }


def parse_logical_term(tokens):
    """
    logical_term = logical_factor { "&&" logical_factor } ;
    """
    node, tokens = parse_logical_factor(tokens)
    while tokens[0]["tag"] == "&&":
        tag = tokens[0]["tag"]
        next_node, tokens = parse_logical_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": next_node}
    return node, tokens


def test_parse_logical_term():
    """
    logical_term = logical_factor { "&&" logical_factor } ;
    """
    print("testing parse_logical_term...")
    assert parse_logical_term(tokenize("x"))[0] == {"tag": "identifier", "value": "x"}
    assert parse_logical_term(tokenize("x&&y"))[0] == {
        "tag": "&&",
        "left": {"tag": "identifier", "value": "x"},
        "right": {"tag": "identifier", "value": "y"},
    }
    assert parse_logical_term(tokenize("x&&y&&z"))[0] == {
        "tag": "&&",
        "left": {
            "tag": "&&",
            "left": {"tag": "identifier", "value": "x"},
            "right": {"tag": "identifier", "value": "y"},
        },
        "right": {"tag": "identifier", "value": "z"},
    }


def parse_logical_expression(tokens):
    """
    logical_expression = logical_term { "||" logical_term } ;
    """
    node, tokens = parse_logical_term(tokens)
    while tokens[0]["tag"] == "||":
        tag = tokens[0]["tag"]
        next_node, tokens = parse_logical_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": next_node}
    return node, tokens


def test_parse_logical_expression():
    """
    logical_expression = logical_term { "||" logical_term } ;
    """
    print("testing parse_logical_expression...")

    assert parse_logical_expression(tokenize("x"))[0] == {
        "tag": "identifier",
        "value": "x",
    }
    assert parse_logical_expression(tokenize("x||y"))[0] == {
        "tag": "||",
        "left": {"tag": "identifier", "value": "x"},
        "right": {"tag": "identifier", "value": "y"},
    }
    assert parse_logical_expression(tokenize("x||y&&z"))[0] == {
        "tag": "||",
        "left": {"tag": "identifier", "value": "x"},
        "right": {
            "tag": "&&",
            "left": {"tag": "identifier", "value": "y"},
            "right": {"tag": "identifier", "value": "z"},
        },
    }


def parse_expression(tokens):
    """
    expression = logical_expression ;
    """
    return parse_logical_expression(tokens)


def test_parse_expression():
    """
    expression = logical_expression ;
    """
    print("testing parse_expression...")
    for s in ["1", "1+1", "1 && 1", "1 < 2"]:
        t = tokenize(s)
        assert parse_expression(t) == parse_logical_expression(t)


# STATEMENTS

def parse_print_statement(tokens):
    """
    print_statement = "print" [ expression ] ;
    """
    assert tokens[0]["tag"] == "print"
    tokens = tokens[1:]
    if tokens[0]["tag"] in ["}", ";", None]:
        # no expression
        return {"tag": "print", "value": None}, tokens
    else:
        value, tokens = parse_expression(tokens)
        return {"tag": "print", "value": value}, tokens


def test_parse_print_statement():
    """
    print_statement = "print" [ expression ] ;
    """
    print("testing parse_print_statement...")
    ast = parse_print_statement(tokenize("print 1"))[0]
    assert ast == {"tag": "print", "value": {"tag": "number", "value": 1}}


def parse_assignment_statement(tokens):
    """
    assignment_statement = expression [ "=" expression ] ;
    """
    target, tokens = parse_expression(tokens)
    if tokens[0]["tag"] == "=":
        tokens = tokens[1:]
        value, tokens = parse_expression(tokens)
        return {"tag": "assign", "target": target, "value": value}, tokens
    return target, tokens

def test_parse_assignment_statement():
    """
    assignment_statement = expression [ "=" expression ] ;
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


def parse_statement(tokens):
    """
    statement = if_statement | while_statement |  function_statement | return_statement | print_statement | assignment_statement ;
    """
    tag = tokens[0]["tag"]
    # note: none of these consumes a token
    # if tag == "{":
    #     return parse_statement_list(tokens)
    # if tag == "if":
    #     return parse_if_statement(tokens)
    # if tag == "while":
    #     return parse_while_statement(tokens)
    # if tag == "function":
    #     return parse_function_statement(tokens)
    # if tag == "return":
    #     return parse_return_statement(tokens)
    if tag == "print":
        return parse_print_statement(tokens)
    return parse_assignment_statement(tokens)


def test_parse_statement():
    """
    statement = if_statement | while_statement | function_statement | return_statement | print_statement | assignment_statement ;
    """
    print("testing parse_statement...")

    # # if statement
    # assert (
    #     parse_statement(tokenize("if(1){print 1}"))[0]
    #     == parse_if_statement(tokenize("if(1){print 1}"))[0]
    # )
    # # # while statement
    # assert (
    #     parse_statement(tokenize("while(1){print 1}"))[0]
    #     == parse_while_statement(tokenize("while(1){print 1}"))[0]
    # )
    # # return statement
    # assert (
    #     parse_statement(tokenize("return 22"))[0]
    #     == parse_return_statement(tokenize("return 22"))[0]
    # )
    # print statement
    assert (
        parse_statement(tokenize("print 1"))[0]
        == parse_print_statement(tokenize("print 1"))[0]
    )
    # # function_statement (syntactic sugar)
    # assert (
    #     parse_statement(tokenize("function x(y){2}"))[0]
    #     == parse_function_statement(tokenize("function x(y){2}"))[0]
    # )
    # assignment statement
    assert (
        parse_statement(tokenize("x=3"))[0]
        == parse_assignment_statement(tokenize("x=3"))[0]
    )

def parse_program(tokens):
    """
    program = [ statement { ";" statement } ] ;
    """
    statements = []
    if tokens[0]["tag"]:
        statement, tokens = parse_statement(tokens)
        statements.append(statement)
        while tokens[0]["tag"] == ";":
            tokens = tokens[1:]
            statement, tokens = parse_statement(tokens)
            statements.append(statement)
    assert (
        tokens[0]["tag"] == None
    ), f"Expected end of input at position {tokens[0]['position']}, got [{tokens[0]}]"
    return {"tag": "program", "statements": statements}, tokens[1:]


def test_parse_program():
    """program = [ statement { ";" statement } ] ;"""
    print("testing parse_program...")
    ast, tokens = parse_program(tokenize("print 1; print 2"))
    assert ast == {
        "tag": "program",
        "statements": [
            {"tag": "print", "value": {"tag": "number", "value": 1}},
            {"tag": "print", "value": {"tag": "number", "value": 2}},
        ],
    }


def parse(tokens):
    ast, tokens = parse_program(tokens)
    return ast


if __name__ == "__main__":
    test_parse_factor()
    test_parse_term()
    test_parse_arithmetic_expression()
    test_parse_relational_expression()
    test_parse_logical_factor()
    test_parse_logical_term()
    test_parse_logical_expression()
    test_parse_assignment_statement()
    test_parse_statement()
    test_parse_program()
    print("done.")
