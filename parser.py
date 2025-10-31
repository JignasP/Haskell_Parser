#!/usr/bin/env python3
"""
Haskell Parser

This module implements a parser for Haskell variable and type declarations.
It processes tokens from the lexer to build an abstract syntax tree (AST)
for Haskell declarations.
"""

import ply.yacc as yacc
from lexer import tokens

# Precedence rules for operators
precedence = (
    ('right', 'ARROW'),
    ('left', 'LBRACKET', 'RBRACKET'),
    ('left', 'LPAREN', 'RPAREN'),
)

class Declaration:
    """Base class for all declaration types."""
    def __str__(self):
        return self.__class__.__name__

class TypeDeclaration(Declaration):
    def __init__(self, name, type_expr):
        self.name = name
        self.type_expr = type_expr
    
    def __str__(self):
        return f"{self.name} :: {self.type_expr}"

class ValueDeclaration(Declaration):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def __str__(self):
        return f"{self.name} = {self.value}"

def p_declaration(p):
    '''declaration : type_declaration
                   | value_declaration
                   | type_and_value'''
    p[0] = p[1]
    print(f"Parsed: {p[0]}")

def p_type_declaration(p):
    'type_declaration : ID DOUBLECOLON type_expr'
    p[0] = TypeDeclaration(p[1], p[3])

def p_value_declaration(p):
    'value_declaration : ID EQUALS expression'
    p[0] = ValueDeclaration(p[1], p[3])

def p_type_and_value(p):
    'type_and_value : ID DOUBLECOLON type_expr ID EQUALS expression'
    if p[1] == p[4]:
        p[0] = (TypeDeclaration(p[1], p[3]), ValueDeclaration(p[4], p[6]))
    else:
        raise SyntaxError(f"Variable name mismatch: {p[1]} vs {p[4]}")

def p_type_expr(p):
    '''type_expr : function_type
                | non_function_type'''
    p[0] = p[1]

def p_non_function_type(p):
    '''non_function_type : simple_type
                        | list_type
                        | tuple_type
                        | unit_type
                        | type_application'''
    p[0] = p[1]

def p_simple_type(p):
    '''simple_type : TYPE
                  | TYPE_CONSTRUCTOR
                  | ID
                  | unit_type'''
    if len(p) == 2:
        p[0] = p[1]

def p_function_type(p):
    'function_type : type_expr ARROW type_expr'
    p[0] = f"{p[1]} -> {p[3]}"

def p_list_type(p):
    'list_type : LBRACKET type_expr RBRACKET'
    p[0] = f"[{p[2]}]"

def p_tuple_type(p):
    'tuple_type : LPAREN type_expr RPAREN'
    p[0] = f"({p[2]})"

def p_unit_type(p):
    '''unit_type : LPAREN_RPAREN
                | LPAREN RPAREN'''
    p[0] = "()"

def p_type_application(p):
    '''type_application : TYPE_CONSTRUCTOR type_expr
                      | TYPE_CONSTRUCTOR LPAREN_RPAREN
                      | TYPE_CONSTRUCTOR LBRACKET type_expr RBRACKET
                      | TYPE_CONSTRUCTOR LPAREN type_expr RPAREN'''
    if len(p) == 3:  # TYPE_CONSTRUCTOR type_expr or TYPE_CONSTRUCTOR ()
        if p[2] == '()':
            p[0] = f"{p[1]} ()"
        else:
            p[0] = f"{p[1]} {p[2]}"
    elif p[2] == '[':  # TYPE_CONSTRUCTOR [type_expr]
        p[0] = f"{p[1]} [{p[3]}]"
    else:  # TYPE_CONSTRUCTOR (type_expr)
        # For IO ()
        if p[3] == '()':
            p[0] = f"{p[1]} ()"
        else:
            p[0] = f"{p[1]} {p[3]}"  # Don't add extra parentheses for type application

def p_expression(p):
    '''expression : literal
                 | identifier
                 | list
                 | parenthesized_expression'''
    p[0] = p[1]

def p_literal(p):
    '''literal : NUMBER
              | STRING'''
    p[0] = p[1]

def p_identifier(p):
    'identifier : ID'
    p[0] = p[1]

def p_list(p):
    'list : LBRACKET list_elements RBRACKET'
    p[0] = f"[{p[2]}]"

def p_list_elements(p):
    '''list_elements : expression
                    | expression COMMA list_elements
                    | empty'''
    if len(p) == 2:
        p[0] = str(p[1])
    elif len(p) == 4:
        p[0] = f"{p[1]}, {p[3]}"

def p_parenthesized_expression(p):
    'parenthesized_expression : LPAREN expression RPAREN'
    p[0] = f"({p[2]})"

def p_empty(p):
    'empty : '
    p[0] = ""

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at token '{p.value}' (type: {p.type}, line: {p.lineno})")
    else:
        raise SyntaxError("Syntax error at end of input")

# Import lexer tokens
from lexer import tokens

# Define tokens for the parser
tokens = tokens + ('TYPE_CONSTRUCTOR',)

# Build the parser
parser = yacc.yacc(debug=False, write_tables=False)

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = f.read()
    else:
        data = sys.stdin.read()
    
    result = parser.parse(data, lexer=lexer)
    print("Parse successful!")
    print("Result:", result)
