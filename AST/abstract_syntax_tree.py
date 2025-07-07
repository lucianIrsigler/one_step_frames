import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from util.formula import getConnectives, findAtomicFormulas
from shunting_yard import shunting_yard,postfix_to_infix
from abstract_operator import AbstractOperator

class Node:
    def __init__(self,arity,value) -> None:
        self.arity = 2
        self.value = value
        if (arity==2):
            self.left=None
            self.right=None
        else:
            self.child= None

    def setLeft(self,left):
        self.left = left
    
    def setRight(self,right):
        self.right = right

    def setChild(self,child):
        self.child = child

    def getLeft(self):
        return self.left
    
    def getRight(self):
        return self.right
    
    def getChild(self):
        return self.child
    
    def getArity(self):
        return self.arity
    
    def __str__(self) -> str:
        return f"Node(arity:{self.arity}, value:{self.value})"
    


class AbstractSyntaxTree:
    def __init__(self,operators:list[AbstractOperator]) -> None:
        self.root = None
        self.nodes = []
        self.operators = operators
        self.operatorsMap = {op.getSymbol(): op for op in operators}
        self.operatorsArityMap = {op.getSymbol(): op.getArity() for op in operators}
        self.variables = []
        self.constants = []
    
    def getRoot(self):
        return self.root
    

    def addNode(self,parent:Node|None,value:AbstractOperator|str,operator=False):
        if (self.root==None):
            if operator:
                assert isinstance(value, AbstractOperator)
                newNode = Node(value.arity,value.symbol)
            else:
                newNode = Node(1,value)
            self.root = newNode


    def findOperator(self,symbol:str)->AbstractOperator|None:
        for op in self.operators:
            if op.getSymbol()==symbol:
                return op
            
        return None
    

    def buildTree(self,formula):
        postfixNotation = shunting_yard(formula)
        postfixNotation = postfixNotation.split()

        connectives = getConnectives(formula)
        counter = 0
                                      

        while counter!=len(connectives):
            symbol = postfixNotation[-1]
            operator = self.findOperator(symbol)
            if (operator!=None):
                self.addNode(None,operator)
            return
        
    def printTree(self):
        print(self.root)

