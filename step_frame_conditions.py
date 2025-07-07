from util.formula import initSubformula
from util.nomial import Nominal
from util.preprocess import preprocess
from AST.abstract_syntax_tree import AbstractSyntaxTree
from AST.abstract_operator import AbstractOperator

operators = [
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
nominalTracker = Nominal()

# TODO : make operators default so less initialization is needed
abstractTree = AbstractSyntaxTree(operators)


def initProcedure(rule:str)->str:
    """Constructs the initial formula from the reduced rule

    Args:
        rule (str): rule to initialize

    Returns:
        str: initialized rule
    """
    output = ""
    premise,conclusion = rule.split("/")
    output += initSubformula(premise)
    output += "=>"
    output += initSubformula(conclusion)
    return output

rule = "#x->y/#x->#y"
formula = initProcedure(rule)
abstractTree.buildTree(formula)

