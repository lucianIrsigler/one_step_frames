import re

logicConnectives = ["=>","<","<'","#","#'","@","@'","~","i*","i!","i","^","|","&","->","<->"]

associativity_map = {
    "=>": "R",
    "<": "L",
    "<'": "L",
    "#": "R",
    "#'": "R",
    "@": "R",
    "@'": "R",
    "~": "R",
    "i*": "R",
    "i!": "R",
    "i": "R",
    "^": "R",
    "|": "L",
    "&": "L",
    "->": "R",
    "<->": "L"
}

# Fixed precedence map with proper hierarchy
precedence_map = {
    "=>": 1,    # implication - lowest precedence
    "<": 3,     # comparison - higher precedence
    "<'": 3,    # comparison
    "#": 5,     # unary operators - highest precedence
    "#'": 5,
    "@": 5,
    "@'": 5,
    "~": 5,
    "i*": 5,
    "i!": 5,
    "i": 5,
    "^": 4,     # conjunction/disjunction
    "|": 2,
    "&": 2,
    "->": 1,    # implication
    "<->": 1    # equivalence
}

pattern = r"i\([a-zA-Z]\)"

def tokenize(formula):
    token_specification = [
        ("I_OPERAND", r"i\([a-zA-Z][a-zA-Z0-9_]*\)"),
        # Fixed: Added '?' to match optional prime after unary operators
        ("UNARY_OP_OPERAND", r"[#@~]'?(?:[a-zA-Z][a-zA-Z0-9_]*)"),
        # Fixed: Updated OPERATOR pattern to properly match prime variants
        ("OPERATOR", r"=>|->|<->|<'|#'|@'|i[*!]?|[#@~^|&<]"),
        ("OPERAND", r"[a-zA-Z][a-zA-Z0-9_]*"),
        ("LPAREN", r"\("),
        ("RPAREN", r"\)"),
        ("SKIP", r"\s+"),
        ("MISMATCH", r"."),
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
    return bool(re.fullmatch(r"i\([a-zA-Z][a-zA-Z0-9_]*\)", token) or 
                # Fixed: Added '?' to match optional prime in operand check
                re.fullmatch(r"[#@~]'?[a-zA-Z][a-zA-Z0-9_]*", token) or 
                re.fullmatch(r"[a-zA-Z][a-zA-Z0-9_]*", token))

def checkOperator(token: str) -> bool:
    return token in logicConnectives

def shunting_yard(formula: str) -> str:
    output = ""
    operatorStack = []
    tokens = tokenize(formula)
    
    print(f"Tokens: {tokens}")  # Debug output
    
    for token in tokens:
        if checkOperand(token):
            output += token + " "
        elif token == '(':
            operatorStack.append(token)
        elif token == ')':
            while operatorStack and operatorStack[-1] != '(':
                output += operatorStack.pop() + " "
            operatorStack.pop()  # pop '('
        elif checkOperator(token):
            while (
                operatorStack
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
            # Determine if it's a unary operator based on context
            # In postfix, unary operators should have exactly 1 operand
            if token in ["#", "#'", "@", "@'", "~", "i*", "i!", "i"] and len(stack) >= 1:
                operand = stack.pop()
                # Add parentheses if operand is complex
                if any(op in operand for op in [" => ", " -> ", " <-> ", " & ", " | ", " < ", " <' ", " ^ "]):
                    stack.append(f"{token}({operand})")
                else:
                    stack.append(f"{token}{operand}")
            elif token == "^" and len(stack) >= 2:
                # ^ can be binary or unary, treat as binary if 2 operands available
                right = stack.pop()
                left = stack.pop()
                
                # Add parentheses based on precedence
                if needs_parentheses(left, token, "left"):
                    left = f"({left})"
                if needs_parentheses(right, token, "right"):
                    right = f"({right})"
                
                stack.append(f"{left} {token} {right}")
            elif token == "^" and len(stack) >= 1:
                # Treat ^ as unary
                operand = stack.pop()
                if any(op in operand for op in [" => ", " -> ", " <-> ", " & ", " | ", " < ", " <' "]):
                    stack.append(f"{token}({operand})")
                else:
                    stack.append(f"{token}{operand}")
            elif len(stack) >= 2:
                # Binary operators
                right = stack.pop()
                left = stack.pop()
                
                # Add parentheses based on precedence to avoid ambiguity
                if needs_parentheses(left, token, "left"):
                    left = f"({left})"
                if needs_parentheses(right, token, "right"):
                    right = f"({right})"
                
                stack.append(f"{left} {token} {right}")
            else:
                raise RuntimeError(f"Not enough operands for operator: {token}")
        else:
            raise RuntimeError(f"Unknown token in postfix: {token}")
    
    if len(stack) != 1:
        raise RuntimeError(f"Invalid postfix expression: {postfix_expr}")
    
    return stack[0]

def needs_parentheses(operand: str, current_op: str, position: str) -> bool:
    """Determine if operand needs parentheses based on operator precedence"""
    # If operand doesn't contain operators, no parentheses needed
    if not any(f" {op} " in operand for op in logicConnectives):
        return False
    
    # Extract the main operator from the operand
    operand_op = None
    for op in sorted(logicConnectives, key=len, reverse=True):
        if f" {op} " in operand:
            operand_op = op
            break
    
    if operand_op is None:
        return False
    
    current_prec = precedence_map.get(current_op, 0)
    operand_prec = precedence_map.get(operand_op, 0)
    current_assoc = associativity_map.get(current_op, "L")
    
    # Add parentheses if operand has lower precedence
    if operand_prec < current_prec:
        return True
    
    # For same precedence, consider associativity
    if operand_prec == current_prec:
        if current_assoc == "L" and position == "right":
            return True
        elif current_assoc == "R" and position == "left":
            return True
    
    return False
