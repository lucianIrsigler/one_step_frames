import re

# Make the dynamic mapping
def get_letter(index):
    char_code = 97 + index

    # Skip 'i', 'v', and 'w'
    skipCharacters = ["i","v","w","u","f"]
    
    skips = {ord(i) for i in skipCharacters}

    while char_code in skips:
        char_code += 1

    # If passed 'z', wrap to 'A', skipping again if needed
    if char_code > ord('z'):
        char_code = 65 + (index - 25)  # Adjust for overflow beyond 'z'
        while char_code in skips:
            char_code += 1

    return chr(char_code)


def generateMapping():
    nominalToSymbol = {}

    # w_0 to w_8 → 'a' to 'h', skip 'i' → 'j' instead
    for i in range(9):
        nominalToSymbol[f"w_{i}"] = get_letter(i)

    # v_0 to v_8 → continue after 'j', total offset of 9
    for i in range(9):
        nominalToSymbol[f"v_{i}"] = get_letter(i + 9)

    # u_0 to u_8 → continue again
    for i in range(9):
        nominalToSymbol[f"u_{i}"] = get_letter(i + 18)

    return nominalToSymbol


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
    "^": "^",
    "|": "|",
    "&": "&"
}


def checkOperand(token:str)->bool:
    return bool(re.fullmatch(r"[a-hj-zA-HJ-Z]", token))


# Text replacement
def replaceCharacters(formula: str,reverse:bool=False) -> str:
    if not reverse:
        for i, j in operator_map.items():
            formula = formula.replace(i, j)
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
    # formula = formula.replace("(", "")
    # formula = formula.replace(")", "")

    return formula


def replaceNominals(formula:str,nominalToSymbol:dict=generateMapping(),reverse:bool=False):
    if not reverse:
        for k,v in nominalToSymbol.items():
            formula = formula.replace(k,v)
    else:
        reversedMap = {v:k for k,v in nominalToSymbol.items()}

        for k,v in reversedMap.items():
            formula = formula.replace(k,v)

    return formula


def cleanUp(formula):
    formula = replaceCharacters(formula,True)
    formula = replaceNominals(formula,reverse=True)
    return formula.replace("{}","")
