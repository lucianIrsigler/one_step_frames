from .regexPatterns import OPERATOR_PATTERN,OPERAND_PATTERN
import re

operatorTranslations={
    # F is for all, E is for exists, R is for relation, f is for function
    # x is old, y is new, z is the rest of form

    "#":"F(y)(R(x,y)[z)",
    "$":"F(y)(R(y,x)[z)",

    "@":"E(y)(R(x,y)^z)",
    "%":"E(y)(R(y,x)^z)",

    "*":"E(y)(f(y)=x&z)",
    "i":"F(y)(y=f(x)^z)",

    "u":"x=yz",
    "<":"[z",

    #TODO might need to change
    ">":"[z",
    ",":"&",
    "|":"|"
}

# Operator/operand functonality
operator_map = {
    "<->": "+",
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
    "^": "&", #TODO might need to change back in case it breaks stuff
    "|": "|",
    ";": ";",
    "&": "&"
}

def checkOperand(token:str)->bool:
    return bool(re.fullmatch(OPERAND_PATTERN, token))


def checkOperator(token: str) -> bool:
    """Check if a token is a valid operator.

    Args:
        token (str): The token to check.

    Returns:
        bool: True if the token is a valid operator, otherwise False.
    """
    return bool(re.fullmatch(OPERATOR_PATTERN, token))



# Text replacement
def replaceCharacters(formula: str,reverse:bool=False) -> str:
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


def replaceCharactersNoParen(formula: str,reverse:bool=False) -> str:
    if not reverse:
        for i, j in operator_map.items():
            formula = formula.replace(i, j)
        
        # formula = formula.replace("(", "")
        # formula = formula.replace(")", "")
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
