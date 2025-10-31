#!/usr/bin/env python3
"""
Haskell Lexer

This module implements a lexer for Haskell variable and type declarations.
It tokenizes Haskell code for the parser to process.
"""

import ply.lex as lex

# Token definitions - order matters for regex matching
TOKENS = [
    # Literals
    'NUMBER',
    'STRING',
    'ID',
    
    # Type-related tokens
    'TYPE',              # Built-in types (Int, String, etc.)
    'TYPE_CONSTRUCTOR',  # Type constructors (Maybe, IO, etc.)
    
    # Operators and delimiters
    'DOUBLECOLON',  # ::
    'ARROW',        # ->
    'EQUALS',       # =
    'LPAREN',       # (
    'RPAREN',       # )
    'LBRACKET',     # [
    'RBRACKET',     # ]
    'COMMA',        # ,
    'LPAREN_RPAREN' # ()
]

tokens = tuple(TOKENS)

# Reserved keywords and types
RESERVED = {
    # Basic types
    'Int': 'TYPE',
    'Integer': 'TYPE',
    'Float': 'TYPE',
    'Double': 'TYPE',
    'Char': 'TYPE',
    'String': 'TYPE',
    'Bool': 'TYPE',
    
    # Type constructors - map to TYPE_CONSTRUCTOR
    'Maybe': 'TYPE_CONSTRUCTOR',
    'Either': 'TYPE_CONSTRUCTOR',
    'IO': 'TYPE_CONSTRUCTOR',
}

# Token regex patterns
# Note: Order is important - more specific patterns first
t_LPAREN_RPAREN = r'\(\)'  # Must come before LPAREN/RPAREN
t_DOUBLECOLON = r'::'
t_ARROW = r'->'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','

def t_TYPE_CONSTRUCTOR(t):
    r'[A-Z][a-zA-Z0-9\']*'
    # Check if it's a built-in type
    if t.value in RESERVED and RESERVED[t.value] == 'TYPE':
        t.type = 'TYPE'
    else:
        t.type = 'TYPE_CONSTRUCTOR'
    return t

def t_ID(t):
    r'[a-z_][a-zA-Z_0-9\']*'
    t.type = 'ID'
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

t_ignore = ' \t'  # Ignore whitespace

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"[Lexer Error] Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':
    import sys
    data = sys.stdin.read()
    lexer.input(data)
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
