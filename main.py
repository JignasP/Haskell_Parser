#!/usr/bin/env python3
"""
Haskell Parser
A simple interactive shell for testing Haskell declarations.
"""

import sys
from lexer import lexer
from parser import parser, TypeDeclaration, ValueDeclaration

def show_help():
    """Display help information."""
    print("\nHASKELL PARSER HELP")
    print("=" * 17)
    print("Type Haskell declarations to parse them.")
    print("\nExamples:")
    print("  x :: Int")
    print("  name = \"Haskell\"")
    print("  add :: Int -> Int -> Int")
    print("  list :: [Int]")
    print("  x :: Int; x = 42")
    print("\nCommands:")
    print("  help  Show this help")
    print("  exit  Quit the program\n")
def process_input(input_str):
    """Process and parse the input."""
    try:
        lexer.lineno = 1
        result = parser.parse(input_str, lexer=lexer)
        if result is not None:
            if isinstance(result, tuple):
                # Handle multiple declarations
                for decl in result:
                    print(f"✓ {decl}")
            else:
                print(f"✓ {result}")
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run the interactive shell."""
    print("Haskell Parser - Type 'help' for examples, 'exit' to quit")
    print("-" * 60)
    
    while True:
        try:
            user_input = input(">>> ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ('exit', 'quit'):
                print("Goodbye!")
                break
                
            if user_input.lower() == 'help':
                show_help()
                continue
                
            process_input(user_input)
            
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
