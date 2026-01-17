"""Lightweight parser and AST utilities for SPASS-style formulas.

This module provides:
- A minimal `Formula` structure parsed from strings like
    "F(w)(R(w,v)->E(k)(...))".
- A navigable `TreeNode`/`FormulaAST` for 0/1/2-arity nodes
    (atoms, quantifiers, binary ops).
- Translators to Prolog/SPASS-friendly terms, e.g.,
    F/E/&/-> to forall/exists/and/implies.

Public entry points commonly used by callers:
- parse_formula(s)
- FormulaAST (with `.root`)
- translateFormulaAST(node)  [legacy]
- translate_formula_ast(node)  [PEP8]
- transformToSPASSInput(s, formula_num="2")  [legacy]
- transform_to_spass_input(s, formula_num="2")  [PEP8]
"""

import re
from ..util.core.regexPatterns import NOMINAL_PATTERN

class Formula:
    def __init__(self, type_, var=None, body=None, left=None, right=None, text=None):
        self.type = type_   # 'forall', 'exists', 'implies', 'and', 'atom'
        self.var = var
        self.body = body
        self.left = left
        self.right = right
        self.text = text

    def __str__(self):
        if self.type == 'forall':
            return f"F({self.var})({self.body})"
        elif self.type == 'exists':
            return f"E({self.var})({self.body})"
        elif self.type == 'implies':
            return f"({self.left}->{self.right})"
        elif self.type == 'and':
            return f"({self.left}&{self.right})"
        elif self.type == 'atom':
            return self.text
        return 'UNKNOWN'

# Strip unnecessary outer parentheses
def strip_outer_parens(s):
    s = s.strip()
    while s.startswith('(') and s.endswith(')'):
        depth = 0
        for i, c in enumerate(s):
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
            if depth == 0 and i != len(s)-1:
                return s  # parentheses not enclosing all
        s = s[1:-1].strip()
    return s

# Recursive parser
def parse_formula(s):
    s = strip_outer_parens(s)

    # Quantifiers
    m = re.match(r'([FE])\(([^)]+)\)\((.*)\)$', s)
    if m:
        q, var, body = m.groups()
        return Formula('forall' if q=='F' else 'exists', var, parse_formula(body))

    # Binary operators: '->' first
    depth = 0
    for i, c in enumerate(s):
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif c == '-' and i+1 < len(s) and s[i+1] == '>' and depth == 0:
            left = parse_formula(s[:i])
            right = parse_formula(s[i+2:])
            return Formula('implies', left=left, right=right)

    # Binary operator '&'
    depth = 0
    for i, c in enumerate(s):
        if c == '(':
            depth += 1
        elif c == ')':
            depth -= 1
        elif c == '&' and depth == 0:
            left = parse_formula(s[:i])
            right = parse_formula(s[i+1:])
            return Formula('and', left=left, right=right)

    # Atom
    return Formula('atom', text=s)


class TreeNode:
    """A proper tree node that can have 0, 1, or 2 children.

    - Atoms have arity 0 and no children.
    - Quantifiers have arity 1 with the quantified body as child.
    - Binary operators (e.g., implies/and) have arity 2 (left/right).
    """
    
    def __init__(self, type_, value=None, var=None, text=None):
        self.type = type_           # 'forall', 'exists', 'implies', 'and', 'atom'
        self.value = value          # string representation
        self.var = var              # variable for quantifiers
        self.text = text            # text for atoms
        self.children = []          # 0, 1, or 2 children
        self.arity = 0
    
    def add_child(self, child):
        """Add a child node and update `arity`. Returns self for chaining."""
        self.children.append(child)
        self.arity = len(self.children)
        return self
    
    def get_child(self, index=0):
        """Get child by index (for quantifiers, use index 0)."""
        if index < len(self.children):
            return self.children[index]
        return None
    
    def get_left(self):
        """Get left child (for binary operators)."""
        return self.get_child(0)
    
    def get_right(self):
        """Get right child (for binary operators)."""
        return self.get_child(1)
    
    def is_leaf(self):
        """Return True if this is a leaf node (atom)."""
        return self.type == 'atom'
    
    def is_quantifier(self):
        """Return True if this is a quantifier (F or E)."""
        return self.type in ('forall', 'exists')
    
    def is_binary(self):
        """Return True if this is a binary operator (implies/and)."""
        return self.type in ('implies', 'and')
    
    def __repr__(self):
        return f"TreeNode({self.type}, arity={self.arity})"


class FormulaAST:
    """Navigable search-tree-like wrapper built from a `Formula` tree.

    Provides consistent access to children via `.children`, `.get_child()`,
    and helpers for binary (`.get_left()/.get_right()`) and quantifier nodes.
    """
    
    def __init__(self, formula):
        self.root = self._build_tree_node(formula)
    
    def _build_tree_node(self, formula):
        """Recursively build `TreeNode` from a `Formula` node."""
        if formula.type in ('forall', 'exists'):
            node = TreeNode(
                formula.type,
                value=str(formula),
                var=formula.var
            )
            child = self._build_tree_node(formula.body)
            node.add_child(child)
            return node
        
        elif formula.type == 'implies':
            node = TreeNode(formula.type, value=str(formula))
            left = self._build_tree_node(formula.left)
            right = self._build_tree_node(formula.right)
            node.add_child(left)
            node.add_child(right)
            return node
        
        elif formula.type == 'and':
            node = TreeNode(formula.type, value=str(formula))
            left = self._build_tree_node(formula.left)
            right = self._build_tree_node(formula.right)
            node.add_child(left)
            node.add_child(right)
            return node
        
        elif formula.type == 'atom':
            node = TreeNode(formula.type, value=str(formula), text=formula.text)
            return node
        
        return None
    
    def get_root(self):
        """Return the root `TreeNode`."""
        return self.root
    
    def print_tree(self, node=None, prefix="", is_last=True):
        """Pretty-print the tree using ASCII connectors."""
        if node is None:
            node = self.root
        
        connector = "+-- " if is_last else "|-- "
        
        if node.type == 'forall':
            print(prefix + connector + f"F({node.var}) (arity: {node.arity})")
        elif node.type == 'exists':
            print(prefix + connector + f"E({node.var}) (arity: {node.arity})")
        elif node.type == 'implies':
            print(prefix + connector + f"'->' (arity: {node.arity})")
        elif node.type == 'and':
            print(prefix + connector + f"'&' (arity: {node.arity})")
        elif node.type == 'atom':
            print(prefix + connector + f"'{node.text}' (arity: {node.arity})")
        
        new_prefix = prefix + ("    " if is_last else "|   ")
        
        # Print all children
        for i, child in enumerate(node.children):
            is_last_child = (i == len(node.children) - 1)
            child_connector = "+-- " if is_last_child else "|-- "
            
            if node.type in ('implies', 'and'):
                # Label left/right for binary operators
                label = "[left]" if i == 0 else "[right]"
                print(new_prefix + child_connector + label)
                child_prefix = new_prefix + ("    " if is_last_child else "|   ")
                self.print_tree(child, child_prefix, is_last_child)
            elif node.type in ('forall', 'exists'):
                # Label child for quantifiers
                print(new_prefix + child_connector + "[child]")
                child_prefix = new_prefix + ("    " if is_last_child else "|   ")
                self.print_tree(child, child_prefix, is_last_child)
    
    def traverse_dfs(self, node=None, callback=None):
        """Depth-first traversal with optional `callback(node)` on visit."""
        if node is None:
            node = self.root
        
        if callback:
            callback(node)
        
        for child in node.children:
            self.traverse_dfs(child, callback)
    
    def find_atoms(self, node=None):
        """Return a list of all atom (leaf) nodes under `node` (or root)."""
        if node is None:
            node = self.root
        
        atoms = []
        
        def collect_atoms(n):
            if n.is_leaf():
                atoms.append(n)
        
        self.traverse_dfs(node, collect_atoms)
        return atoms


def translate_formula_ast(node):
    if node.arity == 0:  # It's an atom
        if "=" in node.value:
            return f"equal({node.text.split('=')[0]},{node.text.split('=')[1]})"
        elif "?" in node.value:
            #R(w_2)?R(w_0)
            #forall([v1],implies(R(w2,v1),R(w0,v1))
            args = node.text.split("?")
            left = args[0]
            right = args[1]

            nominal_left = re.search(NOMINAL_PATTERN, left).group()
            nominal_right = re.search(NOMINAL_PATTERN, right).group()
            return f"forall([x],implies(R({nominal_left},x),R({nominal_right},x)))"
        else:
            return node.text
    elif node.is_quantifier():
        child_result = translate_formula_ast(node.get_child())
        return f"{node.type}([{node.var}],{child_result})"
    elif node.is_binary():
        left_result = translate_formula_ast(node.get_left())
        right_result = translate_formula_ast(node.get_right())
        return f"{node.type}({left_result},{right_result})"
    else:
        raise ValueError("Unknown node type")


def create_SPASS_input(formula_str,formula_num="2"):
    f = parse_formula(formula_str)
    formula_ast = FormulaAST(f)
    return f"formula({translate_formula_ast(formula_ast.root)},{formula_num})."
