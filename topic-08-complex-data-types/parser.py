#!/usr/bin/env python
from tokenizer import tokenize

"""
parser.py
"""

# Grammar 
grammar = """
    parameters = "(" [ identifier { "," identifier } ] ")"
    arguments = "(" [ expression { "," expression } ] ")"
    array_literal = "[" [ expression { "," expression } ] "]"
    object_literal = "{" [ (string | identifier) ":" expression { "," (string | identifier) ":" expression } ] "}"
    expression = <number> | array_literal | object_literal
"""

todo_grammar = """
    function_literal = "function" parameters statement_block ;
    simple_expression = <number> | <string> | <identifier> | "(" expression ")" | "!" expression | "-" expression | function_literal | object_literal | array_literal ;
    complex_expression = simple_expression { ("[" expression "]") | ("." identifier) | arguments } ;
    arithmetic_factor = complex_expression ;
    arithmetic_term = arithmetic_factor { ("*" | "/") arithmetic_factor } ;
    arithmetic_expression = arithmetic_term { ("+" | "-") arithmetic_term } ;
    expression = arithmetic_expression ;
"""

future_grammar = """
    relational_expression = arithmetic_expression { ("<" | ">" | "<=" | ">=" | "==" | "!=") arithmetic_expression } ;
    logical_factor = relational_expression ;
    logical_term = logical_factor { "&&" logical_factor } ;
    logical_expression = logical_term { "||" logical_term } ;
    expression = logical_expression ;
    function_statement = "function" identifier parameters statement_block ;
    statement_block = "{" statement { ";" statement } "}" ;
    assignment_statement = expression [ "=" expression ] ;
    print_statement = "print" [ expression ] ;
    if_statement = "if" "(" expression ")" statement_block [ "else" statement_block ] ;
    while_statement = "while" "(" expression ")" statement_block ;
    statement = statement_block | if_statement | while_statement | print_statement | assignment_statement | function_statement ;
    program = [ statement { ";" statement } ] ;
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

def parse_array_literal(tokens):
    """
    array_literal = "[" [ expression { "," expression } ] "]"
    """
    assert tokens[0]["tag"] == "[", f"Expected '[' but got {tokens[0]}"
    tokens = tokens[1:]
    items = []
    if tokens[0]["tag"] != "]":
        expr, tokens = parse_expression(tokens)
        items.append(expr)
        while tokens[0]["tag"] == ",":
            tokens = tokens[1:]
            expr, tokens = parse_expression(tokens)
            items.append(expr)
    assert tokens[0]["tag"] == "]", f"Expected ']' but got {tokens[0]}"
    return {"tag": "array_literal", "items": items}, tokens[1:]

def test_parse_array_literal():
    """
    array_literal = "[" [ expression { "," expression } ] "]"
    """
    print("testing parse_array_literal...")
    # Test empty array literal
    tokens = tokenize("[]")
    ast, tokens = parse_array_literal(tokens)
    assert ast == {'tag': 'array_literal', 'values': []}
    assert tokens[0]["tag"] is None
    # Test single array literal
    tokens = tokenize("[1]")
    ast, tokens = parse_array_literal(tokens)
    assert ast == {'tag': 'array_literal', 'items': [{'tag': 'number', 'value': 1}]}
    assert tokens[0]["tag"] is None
    tokens = tokenize("[1,2,3]")
    ast, tokens = parse_array_literal(tokens)
    assert ast == {'tag': 'array_literal', 'items': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}]}
    tokens = tokenize("[1,2,3,[4,5]]")
    ast, tokens = parse_array_literal(tokens)
    assert ast == {'tag': 'array_literal', 'items': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}, {'tag': 'array_literal', 'items': [{'tag': 'number', 'value': 4}, {'tag': 'number', 'value': 5}]}]}
    assert tokens[0]["tag"] is None

def parse_object_literal(tokens):
    """
    object_literal = "{" [ (string | identifier) ":" expression { "," (string | identifier) ":" expression } ] "}"
    """
    expected_tag = "{"
    assert tokens[0]["tag"] == expected_tag, f"Expected '{expected_tag}' but got {tokens[0]}"
    tokens = tokens[1:]
    entries = []
    if tokens[0]["tag"] != "}":
        assert tokens[0]["tag"] in ["string","identifier"]
        key = tokens[0]["value"]
        tokens = tokens[1:]
        assert tokens[0]["tag"] == ":"
        tokens = tokens[1:]
        expr, tokens = parse_expression(tokens)
        entries.append({"key":key, "value":expr})
        while tokens[0]["tag"] == ",":
            tokens = tokens[1:]
            assert tokens[0]["tag"] in ["string","identifier"]
            key = tokens[0]["value"]
            tokens = tokens[1:]
            assert tokens[0]["tag"] == ":"
            tokens = tokens[1:]
            expr, tokens = parse_expression(tokens)
            entries.append({"key":key, "value":expr})
    expected_tag = "}"
    assert tokens[0]["tag"] == expected_tag, f"Expected '{expected_tag}' but got {tokens[0]}"
    return {"tag": "object_literal", "entries": entries}, tokens[1:]

def test_parse_object_literal():
    """
    object_literal = "{" [ (string | identifier) ":" expression { "," (string | identifier) ":" expression } ] "}"
    """
    print("testing parse_object_literal...")
    # Test empty object literal
    tokens = tokenize("{}")
    ast, tokens = parse_object_literal(tokens)
    assert ast == {'tag': 'object_literal', 'entries': []}
    assert tokens[0]["tag"] is None
    # Test single array literal
    tokens = tokenize("[1]")
    ast, tokens = parse_array_literal(tokens)
    assert ast == {'tag': 'array_literal', 'entries': [{'tag': 'number', 'value': 1}]}
    assert tokens[0]["tag"] is None
    tokens = tokenize("[1,2,3]")
    ast, tokens = parse_array_literal(tokens)
    assert ast == {'tag': 'array_literal', 'entries': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}]}
    tokens = tokenize("[1,2,3,[4,5]]")
    ast, tokens = parse_array_literal(tokens)
    assert ast == {'tag': 'array_literal', 'entries': [{'tag': 'number', 'value': 1}, {'tag': 'number', 'value': 2}, {'tag': 'number', 'value': 3}, {'tag': 'array_literal', 'entries': [{'tag': 'number', 'value': 4}, {'tag': 'number', 'value': 5}]}]}
    assert tokens[0]["tag"] is None


def parse_expression(tokens):
    """
    expression = <number> | array_literal | object_literal
    """
    token = tokens[0]
    if token["tag"] == "number":
        return {"tag": "number", "value": token["value"]}, tokens[1:]
    if token["tag"] == "[":
        return parse_array_literal(tokens)
    if token["tag"] == "{":
        return parse_object_literal(tokens)
    raise Exception(f"Unexpected token '{token['tag']}' at position {token['position']}.")
    

def test_parse_expression():
    """
    expression = <number> | array_literal | object_literal
    """
    print("testing parse_expression...")
    return True



# --- Grammar Verification Mechanism ---

# Normalize the grammar by stripping whitespace from each nonempty line.
grammar = grammar.split("\n")
grammar = [line.strip() for line in grammar if line.strip() != ""]
print(grammar)

if __name__ == "__main__":
    # List of all test functions.
    test_functions = [
        test_parse_parameters,
        test_parse_arguments,
        test_parse_array_literal,
        test_parse_object_literal,
        test_parse_expression
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