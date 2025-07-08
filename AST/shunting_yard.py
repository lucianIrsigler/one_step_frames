import re

operator_map = {
    "<->": "=",
    "=>": ">",
    "->": "[",
    "<": "<",
    "<'": "]",
    "#'": "$",
    "#": "#",
    "@'": "%",
    "@": "@",
    "~": "~",
    "i*": "*",
    "i!": "!",
    "i": "i",
    "^": "^",
    "|": "|",
    "&": "&"
}

associativity_map = {
    ">": "R",   # => and -> both mapped to >
    "=": "L",   # <-> mapped to =
    "<": "L",
    "[": "L",   # <' mapped to [
    "#": "R",
    "$": "R",   # #' mapped to $
    "@": "R",
    "%": "R",   # @' mapped to %
    "~": "R",
    "*": "R",   # i* mapped to *
    "!": "R",   # i! mapped to !
    "i": "R",
    "^": "R",
    "|": "L",
    "&": "L",
    "]": "L" 
}

precedence_map = {
    ">": 1,    # => and -> both mapped to >
    "=": 1,    # <-> mapped to =
    "|": 2,
    "&": 2,
    "<": 3,
    "[": 3,    # <' mapped to [
    "^": 4,
    "]": 4,
    "#": 6,
    "$": 6,
    "@": 6,
    "%": 6,
    "~": 5,
    "*": 5,
    "!": 5,
    "i": 5
}

regexPatterns={
    "OPERATOR": r"i|[=><\[\]\#\$\@\%\~\*\!\^|&]",  # i operator alone first
    "OPERAND": r"[a-hj-zA-HJ-Z]",                  # operands single letter excluding 'i'
    "SKIP": r"\s+",
    "MISMATCH": r"."
}


def replaceCharacters(formula: str, reverse: bool = False) -> str:
    if not reverse:
        for i, j in operator_map.items():
            formula = formula.replace(i, j)

        formula = formula.replace("(", "")
        formula = formula.replace(")", "")
    else:
        reverse_operator_map = {v: k for k, v in operator_map.items()}
        for i, j in reverse_operator_map.items():
            formula = formula.replace(i, j)

        unary_ops = ["i*", "i!", "i"]
        unary_syms = [operator_map[op] for op in unary_ops]

        prev = None
        while formula != prev:
            prev = formula
            # Add parentheses around non-parenthesized operand
            formula = re.sub(
                rf"({'|'.join(map(re.escape, unary_syms))})(?!\s*\()([a-zA-Z][a-zA-Z0-9_]*)",
                r"\1(\2)",
                formula
            )
        
    return formula


def tokenize(formula):
    #TODO make like list from the dict directly
    token_specification = [
        ("OPERATOR", regexPatterns["OPERATOR"]),  # i operator alone first
        ("OPERAND",  regexPatterns["OPERAND"]),                  # operands single letter excluding 'i'
        ("SKIP", regexPatterns["SKIP"]),
        ("MISMATCH", regexPatterns["MISMATCH"]),
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    get_token = re.compile(tok_regex).match
    pos = 0
    tokens = []
    mo = get_token(formula, pos)
    while mo is not None:
        kind = mo.lastgroup
        value = mo.group()
        if kind == "SKIP":
            pass
        elif kind == "MISMATCH":
            raise RuntimeError(f"Unexpected character: {value} at pos {pos}")
        else:
            tokens.append(value)
        pos = mo.end()
        mo = get_token(formula, pos)
    if pos != len(formula):
        raise RuntimeError(f"Unexpected character at end of input: {formula[pos:]}")
    return tokens


def checkOperand(token: str) -> bool:
    return bool(re.fullmatch(regexPatterns["OPERAND"], token))


def checkOperator(token: str) -> bool:
    return bool(re.fullmatch(regexPatterns["OPERATOR"], token))


def shuntingYardAlgorithm(formula: str) -> str:
    output = ""
    operatorStack = []
    tokens = tokenize(formula)
    # print(tokens)
    
    # Based on your mappings, these are unary prefix operators
    unary_operators = {"#", "$", "@", "%", "~", "*", "!", "i"}
    
    for token in tokens:
        if checkOperand(token):
            output += token + " "
            # After an operand, pop any pending unary operators
            while operatorStack and operatorStack[-1] in unary_operators:
                output += operatorStack.pop() + " "
        elif token == '(':
            operatorStack.append(token)
        elif token == ')':
            while operatorStack and operatorStack[-1] != '(':
                output += operatorStack.pop() + " "
            operatorStack.pop()  # pop '('
        elif checkOperator(token):
            if token in unary_operators:
                # Unary operators - just push onto stack, will be popped after operand
                operatorStack.append(token)
            else:
                # Binary operators
                while (
                    operatorStack
                    and operatorStack[-1] != '('
                    and checkOperator(operatorStack[-1])
                    and (
                        (associativity_map[token] == "L" and precedence_map[token] <= precedence_map[operatorStack[-1]])
                        or
                        (associativity_map[token] == "R" and precedence_map[token] < precedence_map[operatorStack[-1]])
                    )
                ):
                    output += operatorStack.pop() + " "
                operatorStack.append(token)
        else:
            raise RuntimeError(f"Unknown token: {token}")
    
    while operatorStack:
        output += operatorStack.pop() + " "
    
    return output.strip()

def postfix_to_infix(postfix_expr: str) -> str:
    """Convert postfix expression back to infix notation"""
    tokens = postfix_expr.split()
    stack = []
    
    for token in tokens:
        if checkOperand(token):
            stack.append(token)
        elif checkOperator(token):
            unary_operators = {"#", "$", "@", "%", "~", "*", "!", "i"}
            if token in unary_operators:
                if len(stack) < 1:
                    raise RuntimeError(f"Not enough operands for unary operator: {token}")
                operand = stack.pop()
                if any(op in operand for op in [" => ", " -> ", " <-> ", " & ", " | ", " < ", " <' ", " ^ "]):
                    stack.append(f"{token}({operand})")
                else:
                    stack.append(f"{token}{operand}")
            elif len(stack) >= 2:
                # Binary operators
                right = stack.pop()
                left = stack.pop()
                stack.append(f"{left} {token} {right}")
            else:
                raise RuntimeError(f"Not enough operands for operator: {token}")
        else:
            raise RuntimeError(f"Unknown token in postfix: {token}")
    
    if len(stack) != 1:
        raise RuntimeError(f"Invalid postfix expression: {postfix_expr}")
    
    return stack[0]


def shuntingYard(formula:str):
    inputFormula = replaceCharacters(formula)
    postfix = shuntingYardAlgorithm(inputFormula)
    reverted = replaceCharacters(postfix, True)
    return reverted
