
NOMINAL_PATTERN = r"\b[uwv](?:_\d+)?\b|i\(\b[uwv](?:_\d+)?\b\)"
NOMINAL_PATTERN_STRICT = r"\b[uwv](?:_\d+)?\b"
VARIABLE_PATTERN = r"[a-hj-tx-z](?:_\d+)?"
OPERATOR_PATTERN = r"i|[=><\[\]\#\$\@\%\~\*\!\^|&|,]"
OPERAND_PATTERN = r"[a-hj-zA-HJ-Z](?:_\d+)?"

# simplify
EQUALITY_PATTERN = r'\b[uwv]_\d+=\b[uwv]_\d+'
RELATIONS_PATTERN = r'\b[R|f]\([^()]*\)'
QUANTIFIERS_PATTERN = r'\b[F|E]\([^()]*\)'
SUBSET_RELATION_PATTERN = r'R\([^,]+,(\w+)\)\[R\([^,]+,\1\)'
SUBSET_ARGUMENTS_PATTERN = r'R\(([^,]+),(\w+)\)\[R\(([^,]+),\2\)'