import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from util.formula import getConnectives, findAtomicFormulas
from AST.shunting_yard import shuntingYard
from AST.abstract_operator import AbstractOperator
from AST.AST_error import ASTError


defaultOperators = operators = [
    # perf 2
    AbstractOperator("=>",2,2),

    # perf 1
    AbstractOperator("<",2,1),
    AbstractOperator("<'",2,1),

    #perf 0
    AbstractOperator("#",1),
    AbstractOperator("#'",1),
    AbstractOperator("@",1),
    AbstractOperator("@'",1),
    AbstractOperator("~",1),
    AbstractOperator("i*",1),
    AbstractOperator("i!",1),
    AbstractOperator("i",1),

    AbstractOperator("^",2),
    AbstractOperator("&",2),
    AbstractOperator("->",2),
    AbstractOperator("<->",2),
]


class Node:
    def __init__(self, arity, value) -> None:
        self.arity = arity  # Fix: use the parameter instead of hardcoding 2
        self.value = value
        if (arity == 2):
            self.left = None
            self.right = None
        else:
            self.child = None
    
    def setLeft(self, leftNode):
        self.left = leftNode
    
    def setRight(self, rightNode):
        self.right = rightNode
    
    def setChild(self, childNode):
        self.child = childNode
    
    def __str__(self) -> str:
        return f"Node(arity:{self.arity}, value:{self.value})"


class AbstractSyntaxTree:
    def __init__(self, operators: list[AbstractOperator]=defaultOperators) -> None:
        self.root = None
        self.nodes = []
        self.operators = operators
        self.operatorsMap = {op.getSymbol(): op for op in operators}
        self.operatorsArityMap = {op.getSymbol(): op.getArity() for op in operators}
        self.variables = []
        self.constants = []
    
    def getRoot(self):
        return self.root
    
    def findOperator(self, symbol: str) -> AbstractOperator | None:
        for op in self.operators:
            if op.getSymbol() == symbol:
                return op
        return None
    

    def buildTree(self, formula: str):
        """Build the AST from a formula string"""
        postfixNotation = shuntingYard(formula).split()
        if not postfixNotation:
            raise ASTError("Cannot build tree from empty postfix notation")
        
        # Use a stack-based approach to build the tree from postfix notation
        stack = []
        
        for token in postfixNotation:
            operator = self.findOperator(token)
            
            if operator is not None:
                # It's an operator
                arity = operator.getArity()
                node = Node(arity, token)
                
                if arity == 1:
                    # Unary operator - needs 1 operand
                    if len(stack) < 1:
                        raise ASTError(f"Not enough operands for unary operator {token}")
                    node.child = stack.pop()
                elif arity == 2:
                    # Binary operator - needs 2 operands
                    if len(stack) < 2:
                        raise ASTError(f"Not enough operands for binary operator {token}")
                    # Note: In postfix, the right operand is popped first
                    node.right = stack.pop()
                    node.left = stack.pop()
                else:
                    raise ASTError(f"Unsupported arity {arity} for operator {token}")
                
                stack.append(node)
            else:
                # It's an operand (variable or constant)
                node = Node(0, token)  # Operands have arity 0
                stack.append(node)
        
        if len(stack) != 1:
            raise ASTError(f"Invalid expression: stack has {len(stack)} elements after processing")
        
        self.root = stack[0]
        return self.root
    
    def printTree(self):
        """Print the tree structure in a readable format"""
        if self.root is None:
            print("Empty tree")
            return
        
        print("Abstract Syntax Tree:")
        print("=" * 30)
        self._printNode(self.root, "", True)
        print("=" * 30)
    
    def _printNode(self, node: Node, prefix: str, isLast: bool):
        """Helper method to recursively print nodes with tree structure"""
        if node is None:
            return
        
        # Print current node
        connector = "└── " if isLast else "├── "
        print(f"{prefix}{connector}'{node.value}' (arity: {node.arity})")
        
        # Prepare prefix for children
        extension = "    " if isLast else "│   "
        new_prefix = prefix + extension
        
        # Print children based on arity
        if node.arity == 1:
            # Unary operator - has one child
            if hasattr(node, 'child') and node.child is not None:
                self._printNode(node.child, new_prefix, True)
        elif node.arity == 2:
            # Binary operator - has left and right children
            if hasattr(node, 'left') and hasattr(node, 'right'):
                # Print left child first (not last if right exists)
                has_right = node.right is not None
                if node.left is not None:
                    self._printNode(node.left, new_prefix, not has_right)
                
                # Print right child (always last)
                if node.right is not None:
                    self._printNode(node.right, new_prefix, True)
    
    def printTreeCompact(self):
        """Print a more compact representation of the tree"""
        if self.root is None:
            print("Empty tree")
            return
        
        print("Compact Tree Representation:")
        print(self._nodeToString(self.root))
    
    def _nodeToString(self, node: Node) -> str:
        """Convert a node and its children to a string representation"""
        if node is None:
            return "None"
        
        if node.arity == 0:
            # Leaf node (variable/constant)
            return str(node.value)
        elif node.arity == 1:
            # Unary operator
            if hasattr(node, 'child') and node.child is not None:
                return f"{node.value}({self._nodeToString(node.child)})"
            else:
                return f"{node.value}(?)"
        elif node.arity == 2:
            # Binary operator
            left_str = "?" if not hasattr(node, 'left') or node.left is None else self._nodeToString(node.left)
            right_str = "?" if not hasattr(node, 'right') or node.right is None else self._nodeToString(node.right)
            return f"({left_str} {node.value} {right_str})"
        else:
            return str(node.value)
        


if __name__=="__main__":
    tempTree = AbstractSyntaxTree()
    formula = "#x<y=>#x<#y"
    tempTree.buildTree(formula)
    tempTree.printTree()
