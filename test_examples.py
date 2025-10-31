#!/usr/bin/env python3
"""
Haskell Parser Test Suite

This script tests the Haskell lexer and parser with various valid and invalid inputs.
"""

import sys
from lexer import lexer
from parser import parser, TypeDeclaration, ValueDeclaration

# Test cases with expected results
TEST_CASES = [
    # Type declarations
    ("x :: Int", TypeDeclaration("x", "Int")),
    ("name :: String", TypeDeclaration("name", "String")),
    ("isValid :: Bool", TypeDeclaration("isValid", "Bool")),
    ("piValue :: Double", TypeDeclaration("piValue", "Double")),
    
    # Function types
    ("add :: Int -> Int -> Int", TypeDeclaration("add", "Int -> Int -> Int")),
    ("map :: (a -> b) -> [a] -> [b]", 
     TypeDeclaration("map", "(a -> b) -> [a] -> [b]")),
    
    # List types
    ("numbers :: [Int]", TypeDeclaration("numbers", "[Int]")),
    ("chars :: [Char]", TypeDeclaration("chars", "[Char]")),
    
    # Parameterized types and unit
    ("maybeVal :: Maybe Int", TypeDeclaration("maybeVal", "Maybe Int")),
    ("main :: IO ()", TypeDeclaration("main", "IO ()")),
    ("empty :: ()", TypeDeclaration("empty", "()")),
    
    # Value declarations
    ("answer = 42", ValueDeclaration("answer", "42")),
    ("greeting = \"Hello\"", ValueDeclaration("greeting", "Hello")),
    ("pi = 3.14159", ValueDeclaration("pi", "3.14159")),
    ("primes = [2, 3, 5, 7, 11]", ValueDeclaration("primes", "[2, 3, 5, 7, 11]")),
]

# Invalid test cases
INVALID_CASES = [
    "42 = x",  # Invalid assignment
    ":: Int",  # Missing identifier
    "x =",     # Incomplete expression
    "x :: ",   # Incomplete type
    "x = 1 2",  # Invalid expression
]

def run_tests():
    """Run all test cases and report results."""
    print("=" * 80)
    print(f"{'HASKELL PARSER TEST SUITE':^80}")
    print("=" * 80)
    
    # Test valid cases
    print("\nTESTING VALID DECLARATIONS")
    print("-" * 80)
    
    passed = 0
    for i, (test_input, expected) in enumerate(TEST_CASES, 1):
        try:
            result = parser.parse(test_input, lexer=lexer)
            
            # Check if result matches expected type and basic structure
            test_passed = False
            if isinstance(result, type(expected)):
                if hasattr(result, 'name') and hasattr(expected, 'name'):
                    if result.name == expected.name:
                        test_passed = True
                elif isinstance(result, tuple) and isinstance(expected, tuple):
                    # For type_and_value declarations
                    if len(result) == len(expected):
                        test_passed = all(
                            r.name == e.name and str(r) == str(e)
                            for r, e in zip(result, expected)
                        )
            
            if test_passed:
                status = "PASSED"
                passed += 1
            else:
                status = f"FAILED (got: {result}, expected: {expected})"
            
            print(f"[{i:2d}] {test_input:40} -> {status}")
            
        except Exception as e:
            print(f"[{i:2d}] {test_input:40} -> ERROR: {str(e)}")
    
    # Test invalid cases
    print("\nTESTING INVALID DECLARATIONS")
    print("-" * 80)
    
    invalid_passed = 0
    for i, test_input in enumerate(INVALID_CASES, 1):
        try:
            result = parser.parse(test_input, lexer=lexer)
            print(f"[I{i:2d}] {test_input:40} -> FAILED (should be invalid)")
        except Exception:
            print(f"[I{i:2d}] {test_input:40} -> PASSED (correctly rejected)")
            invalid_passed += 1
    
    # Print summary
    total = len(TEST_CASES)
    print("\n" + "=" * 80)
    print(f"SUMMARY: {passed}/{total} valid tests passed")
    print(f"         {invalid_passed}/{len(INVALID_CASES)} invalid tests passed")
    print("=" * 80)
    
    return passed == total and invalid_passed == len(INVALID_CASES)

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
