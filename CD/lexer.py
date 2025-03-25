import re
from typing import List, Literal, Tuple, Union

# Define token types
TokenType = Union[
    Tuple[Literal["KEYWORD"], str],
    Tuple[Literal["IDENTIFIER"], str],
    Tuple[Literal["INTEGER"], str],
    Tuple[Literal["OPERATOR"], str],
    Tuple[Literal["STRING"], str],
    Tuple[Literal["CHAR"], str],
    Tuple[Literal["COMMENT"], str],
]

# C keywords
KEYWORDS = {
    'int', 'void', 'float', 'char', 'string', 'return', 'if', 'else', 
    'while', 'for', 'do', 'break', 'continue', 'switch', 'case', 'default'
}

# Operators - sorted by length to handle multi-character operators first
OPERATORS = {
    '>>=', '<<=', '==', '!=', '+=', '-=', '*=', '/=', '%=', '>>', '<<',
    '&&', '||', '++', '--', '>=', '<=', '->', '=', '>', '<', '!', '~',
    '+', '-', '*', '/', '%', '&', '|', '^', '?', ':', ',', ';', '.',
    '(', ')', '[', ']', '{', '}'
}

def lexer(input_str: str) -> List[TokenType]:
    tokens = []
    i = 0
    n = len(input_str)
    
    while i < n:
        # Skip whitespace
        if input_str[i].isspace():
            i += 1
            continue
        
        # Handle comments
        if input_str[i:i+2] == '//':
            end = input_str.find('\n', i)
            if end == -1:
                end = n
            tokens.append(('COMMENT', input_str[i:end]))
            i = end
            continue
        
        if input_str[i:i+2] == '/*':
            end = input_str.find('*/', i)
            if end == -1:
                end = n
            tokens.append(('COMMENT', input_str[i:end+2]))
            i = end + 2
            continue
        
        # Handle string literals
        if input_str[i] == '"':
            j = i + 1
            while j < n and input_str[j] != '"':
                if input_str[j] == '\\':  # Skip escape sequences
                    j += 1
                j += 1
            if j >= n:
                raise ValueError("Unterminated string literal")
            tokens.append(('STRING', input_str[i:j+1]))
            i = j + 1
            continue
        
        # Handle character constants
        if input_str[i] == "'":
            j = i + 1
            while j < n and input_str[j] != "'":
                if input_str[j] == '\\':  # Skip escape sequences
                    j += 1
                j += 1
            if j >= n:
                raise ValueError("Unterminated character constant")
            tokens.append(('CHAR', input_str[i:j+1]))
            i = j + 1
            continue
        
        # Handle numbers
        if input_str[i].isdigit():
            j = i
            while j < n and input_str[j].isdigit():
                j += 1
            tokens.append(('INTEGER', input_str[i:j]))
            i = j
            continue
        
        # Handle identifiers and keywords
        if input_str[i].isalpha() or input_str[i] == '_':
            j = i
            while j < n and (input_str[j].isalnum() or input_str[j] == '_'):
                j += 1
            word = input_str[i:j]
            if word in KEYWORDS:
                tokens.append(('KEYWORD', word))
            else:
                tokens.append(('IDENTIFIER', word))
            i = j
            continue
        
        # Handle operators
        matched = False
        for op in sorted(OPERATORS, key=len, reverse=True):
            if input_str.startswith(op, i):
                tokens.append(('OPERATOR', op))
                i += len(op)
                matched = True
                break
        
        if not matched:
            raise ValueError(f"Unexpected character: {input_str[i]}")
    
    return tokens

def print_tokens(tokens: List[TokenType]):
    for token_type, value in tokens:
        print(f"{token_type:12}: {value}")

code = """
int main() {
    // This is a comment
    printf("Hello\\n");
    return 0;
    /* This is a
        multi-line comment */
    char c = 'x';
    int x = 42;
    x += 1;
}
"""
    
tokens = lexer(code)
print_tokens(tokens)
