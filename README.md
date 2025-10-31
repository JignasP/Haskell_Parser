# Haskell Parser with PLY

A simple Haskell parser that handles variable declarations, type signatures, and basic expressions. Built using Python's PLY (Python Lex-Yacc) library.

## What's Inside?

This project contains:
- **Lexer**: Breaks down code into tokens
- **Parser**: Understands the structure of Haskell code
- **Interactive Shell**: Test the parser in real-time

## Features

### Type System
- Basic types: `Int`, `String`, `Bool`, `Char`, `Float`, `Double`
- Type constructors: `Maybe`, `Either`, `IO`
- Function types: `->`
- List types: `[Int]`, `[Char]`
- Unit type: `()`

### Declarations
- Type signatures: `x :: Int`
- Value bindings: `x = 42`
- Combined: `x :: Int; x = 42`

### Expressions
- Numbers: `42`, `3.14`
- Strings: `"hello"`
- Lists: `[1, 2, 3]`
- Variables: `x`, `myVar`

## How It Works

### Lexer (lexer.py)
- Converts text into tokens
- Handles Haskell-specific syntax like `::` and `->`
- Differentiates between types, variables, and literals

### Parser (parser.py)
- Validates syntax according to Haskell's grammar
- Handles operator precedence and associativity
- Builds an Abstract Syntax Tree (AST)

#### Parser Precedence Rules
```python
precedence = (
    ('right', 'ARROW'),         # Function arrow is right-associative
    ('left', 'LBRACKET', 'RBRACKET'),  # List brackets
    ('left', 'LPAREN', 'RPAREN'),      # Parentheses
)
```

### Example Parse Tree
For `map :: (a -> b) -> [a] -> [b]`:
```
TypeDeclaration
├── name: "map"
└── type_expr: FunctionType
    ├── param_type: FunctionType
    │   ├── param_type: TypeVar "a"
    │   └── return_type: TypeVar "b"
    └── return_type: FunctionType
        ├── param_type: ListType
        │   └── element_type: TypeVar "a"
        └── return_type: ListType
            └── element_type: TypeVar "b"
```

## Getting Started

1. **Install Dependencies**
   ```bash
   pip install ply
   ```

2. **Run the Interactive Shell**
   ```bash
   python main.py
   ```

3. **Try These Examples**
   ```haskell
   -- Type declarations
   x :: Int
   name :: String
   add :: Int -> Int -> Int
   
   -- Value declarations
   x = 42
   greeting = "Hello, Haskell!"
   
   -- Combined
   x :: Int; x = 42
   ```


## Features

This parser can handle:
- **Type declarations**: `x :: Int`, `add :: Int -> Int -> Int`
- **Value declarations**: `x = 42`, `name = "Haskell"`
- **List types**: `list :: [Int]`, `chars :: [Char]`
- **Function types**: `add :: Int -> Int -> Int`
- **Parameterized types**: `maybeVal :: Maybe Int`
- **Numeric and string literals**

## Supported Haskell Types

- `Int`, `Integer`
- `Float`, `Double`
- `Char`, `String`
- `Bool`
- `Maybe`, `Either`
- `IO`

## File Structure

- **lexer.py**: Defines tokens and lexical rules for Haskell syntax
- **parser.py**: Defines grammar rules for Haskell declarations
- **main.py**: Main program to test the parser interactively

## Grammar Rules

The parser implements the following grammar:

```
declaration → type_declaration
            | value_declaration
            | type_and_value

type_declaration → ID :: type_expr

value_declaration → ID = expression

type_expr → TYPE
          | ID
          | type_expr -> type_expr
          | [type_expr]
          | (type_expr)
          | TYPE type_expr
          | ID type_expr

expression → NUMBER
           | STRING
           | ID
           | [list_elements]
           | (expression)
```

## Usage

Run the parser:
```bash
python main.py
```

### Example Inputs

Valid declarations:
```haskell
x :: Int
y = 42
name :: String
name = "Haskell"
add :: Int -> Int -> Int
list :: [Int]
maybeVal :: Maybe Int
result :: IO ()
```

## How It Works

1. **Lexer** (`lexer.py`): Breaks input into tokens
   - Identifies keywords, operators, identifiers, literals
   - Recognizes Haskell-specific syntax like `::` and `->`

2. **Parser** (`parser.py`): Validates syntax according to grammar
   - Checks if declarations follow Haskell syntax rules
   - Handles type signatures and value assignments

3. **Main** (`main.py`): Interactive testing interface
   - Accepts user input
   - Displays parsing results

## Notes

- This is a simplified parser focusing on variable declarations
- It doesn't handle full Haskell syntax (pattern matching, guards, etc.)
- Designed for educational purposes following the PLY tutorial structure
