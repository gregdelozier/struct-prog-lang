---
marp: true
theme: default
---

# Recursive Descent Parser for a Simple Language
## With Support for Advanced Data Types and Functions
Gregory DeLozier

---

## Parser Design Overview

- Token-based recursive descent parser
- Built from EBNF grammar
- Each rule has:
  - EBNF definition
  - Matching parse function
  - Unit tests for coverage
- Evaluator supports early return propagation

---

## Parser Structure

- Tokenizer (separate module)
- `parse_<rule>` functions
- Test functions verify each rule
- AST is constructed as nested dictionaries

Example AST node:
~~~
{ "tag": "number", "value": 42 }
~~~

---

## Expressions

- Simple to complex, evaluated with precedence

~~~
expression
  → logical_expression
    → logical_term ('||' logical_term)*
      → logical_factor ('&&' logical_factor)*
        → relational_expression
          → arithmetic_expression
            → arithmetic_term ('*' | '/')*
              → complex_expression
                → simple_expression
~~~

---

## Arrays

- Defined as square-bracketed lists

EBNF:
~~~
array = "[" [ expression { "," expression } ] "]"
~~~

Example:
~~~
[1, 2, 3]
→
{ "tag": "array", "values": [...] }
~~~

---

## Objects

- JSON-like dictionary literals

EBNF:
~~~
object = "{" [ (string | identifier) ":" expression { "," (string | identifier) ":" expression } ] "}"
~~~

Example:
~~~
{x: 1, y: 2}
→
{ "tag": "object", "values": [{ "key": "x", "value": ... }] }
~~~

---

## First-Class Functions

- Functions can be created, passed, and returned

EBNF:
~~~
function = "function" parameters block
~~~

Example:
~~~
function(x) { return x + 1 }
→
{ "tag": "function", "parameters": [...], "body": [...] }
~~~

---

## Function Statements

- Declared with an identifier

EBNF:
~~~
function_statement = "function" identifier parameters block
~~~

Desugared to:
~~~
identifier = function(...) {...}
~~~

---

## Return Statements

- Support early exits from functions

EBNF:
~~~
return_statement = "return" [ expression ]
~~~

Runtime:
- `evaluate_*` returns `(value, returning)`
- Callers check `returning` to propagate upward

---

## Function Evaluation

~~~
function(x) {
  if (x > 10) { return 42 }
  return x
}
~~~

Evaluation returns:
~~~
(value, returning) = (42, True)
→ call site detects and exits
~~~

---

## Summary

- Parser supports:
  - Expressions, statements, and control flow
  - Arrays and objects
  - First-class and named functions
  - Early return chaining

## Possible Additions
- `import` statements
- Comments in tokenizer
- Optional namespaces

