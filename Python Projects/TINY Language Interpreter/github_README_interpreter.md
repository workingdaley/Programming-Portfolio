# TINY Language Interpreter (Python)

A lexical analyzer, recursive descent parser, and interpreter for a simplified arithmetic language ("TINY"), translated from a provided C++ reference implementation (`parser.c`) into Python as part of a Comparative Programming Languages course.

## What It Does

Given a `.tiny` source file, the program:

1. **Lexically analyzes** the input character by character, classifying tokens as identifiers, integer literals, operators (`+ - * /`), parentheses, semicolons, the assignment operator, and the `PRINT` keyword.
2. **Parses** the token stream using recursive descent (`stmtList -> stmt -> expr -> term -> factor`), correctly handling operator precedence (multiplication and division before addition and subtraction) and parenthesized sub-expressions.
3. **Evaluates** each statement as it's parsed, supporting variable assignment and print statements, using a symbol table (`varMap`) to store and retrieve variable values.
4. **Handles errors**, including undefined identifiers, malformed expressions, missing semicolons, and empty input files.

## Usage

```
python parser_2712207.py <input_file>.tiny
```

## Notable Implementation Challenges

Translating this from C++ to Python surfaced some real language differences worth documenting:

- **`match-case` vs. `switch-case`:** Python's `match-case` behaves differently from C++'s `switch-case` when matching against a variable's value rather than a literal pattern. This caused a subtle bug in the lexer where the first case matched unconditionally regardless of the actual value. Resolved by reverting that section to an `if-elif-else` structure.
- **EOF representation:** C++ conventionally represents end-of-file as `-1`. Python's `file.read()` returns an empty string (`""`) at EOF instead, which caused an infinite loop until the comparison logic was corrected.
- **No pointers in Python:** The original C++ implementation relied on pointers to return values by reference. Python required a different approach to returning and storing variable values correctly, which initially introduced a bug where printed values didn't match the stored values.

A full writeup of the debugging process and design decisions is included in `Parser_2712207_Report.pdf` in this folder.

## Skills Demonstrated

- Lexical analysis and tokenization
- Recursive descent parsing and grammar implementation
- Expression evaluation with correct operator precedence
- Symbol table management
- Cross-language translation and debugging (C++ to Python)
