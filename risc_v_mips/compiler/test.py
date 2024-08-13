import re

def tokenize(code):
    token_specification = [
        ('NUMBER',    r'\d+(\.\d*)?'),  # Integer or decimal number
        ('IDENT',     r'[A-Za-z_]\w*'), # Identifiers
        ('OP',        r'[+\-*/]'),      # Arithmetic operators
        ('EQ',        r'=='),           # Equality operator
        ('ASSIGN',    r'='),            # Assignment operator
        ('END',       r';'),            # Statement terminator
        ('SKIP',      r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH',  r'.'),            # Any other character
    ]
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(token_regex).match
    line_no = 1
    line_start = 0
    tokens = []
    mo = get_token(code)
    while mo is not None:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            value = float(value) if '.' in value else int(value)
        elif kind == 'IDENT' and value in ('if', 'else', 'while'):
            kind = value.upper()
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError(f'{value!r} unexpected on line {line_no}')
        tokens.append((kind, value))
        mo = get_token(code, mo.end())
    return tokens

code = "int x = 10 + 20;"
tokens = tokenize(code)
print(tokens)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type=None):
        if expected_type and self.tokens[self.pos][0] != expected_type:
            raise RuntimeError(f'Expected {expected_type}')
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse(self):
        return self.parse_statement()

    def parse_statement(self):
        token = self.consume('IDENT')
        if token[1] != 'int':
            raise RuntimeError(f'Unexpected token {token}')
        var_name = self.consume('IDENT')[1]
        self.consume('ASSIGN')
        expr = self.parse_expression()
        self.consume('END')
        return ('ASSIGN', var_name, expr)

    def parse_expression(self):
        term = self.parse_term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] == 'OP':
            op = self.consume('OP')[1]
            right = self.parse_term()
            term = ('BINOP', op, term, right)
        return term

    def parse_term(self):
        token = self.consume()
        if token[0] == 'NUMBER':
            return ('NUM', token[1])
        elif token[0] == 'IDENT':
            return ('VAR', token[1])
        else:
            raise RuntimeError(f'Unexpected token {token}')

tokens = [('IDENT', 'int'), ('IDENT', 'x'), ('ASSIGN', '='), ('NUMBER', 10), ('OP', '+'), ('NUMBER', 20), ('END', ';')]
parser = Parser(tokens)
ast = parser.parse()
print(ast)


def generate_code(node):
    if node[0] == 'ASSIGN':
        _, var_name, expr = node
        code = generate_code(expr)
        code.append(f'sw $t0, {var_name}')
        return code
    elif node[0] == 'BINOP':
        _, op, left, right = node
        code_left = generate_code(left)
        code_right = generate_code(right)
        code = code_left + code_right
        if op == '+':
            code.append('add $t0, $t0, $t1')
        elif op == '-':
            code.append('sub $t0, $t0, $t1')
        elif op == '*':
            code.append('mul $t0, $t0, $t1')
        elif op == '/':
            code.append('div $t0, $t0, $t1')
        return code
    elif node[0] == 'NUM':
        return [f'li $t0, {node[1]}']
    elif node[0] == 'VAR':
        return [f'lw $t0, {node[1]}']

ast = ('ASSIGN', 'x', ('BINOP', '+', ('NUM', 10), ('NUM', 20)))
code = generate_code(ast)
for line in code:
    print(line)